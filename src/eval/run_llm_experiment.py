from __future__ import annotations

import argparse
import concurrent.futures
import csv
import json
import os
import re
import threading
import time
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any

from src.common import RUBRIC_DIMENSIONS, UNIFIED_SYSTEM_PROMPT_T0, blind_payload

EVALUATION_MODES = ["blinded_T0", "unblinded_T0", "social_cue_pos", "social_cue_neg"]
GEMINI_MODEL = "gemini-3.5-flash-lite"

CSV_COLUMNS = [
    "record_id",
    "track",
    "evaluation_mode",
    "run_idx",
    "composite_score",
    "predicted_invest",
    "predicted_invest_prob",
    "predicted_survival_prob",
    "confidence",
    "key_risk_flag",
    *RUBRIC_DIMENSIONS,
]


def call_gemini_json(
    prompt: str,
    temperature: float = 0.2,
    max_retries: int = 8,
    model: str | None = None,
) -> dict[str, Any]:
    """Call Gemini REST API and parse structured JSON output."""
    api_key = os.environ.get("GEMINI_API_KEY", "").strip()
    if not api_key:
        raise RuntimeError("GEMINI_API_KEY environment variable is not set.")

    model_name = model or GEMINI_MODEL
    url = (
        f"https://generativelanguage.googleapis.com/v1beta/models/"
        f"{model_name}:generateContent?key={api_key}"
    )
    payload = {
        "systemInstruction": {"parts": [{"text": UNIFIED_SYSTEM_PROMPT_T0}]},
        "contents": [{"role": "user", "parts": [{"text": prompt}]}],
        "generationConfig": {
            "temperature": temperature,
            "responseMimeType": "application/json",
        },
    }
    body = json.dumps(payload).encode("utf-8")

    last_err: Exception | None = None
    for attempt in range(max_retries):
        req = urllib.request.Request(
            url,
            data=body,
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        try:
            with urllib.request.urlopen(req, timeout=60) as resp:
                resp_data = json.loads(resp.read().decode("utf-8"))
            parts = resp_data["candidates"][0]["content"]["parts"]
            text = "".join(p.get("text", "") for p in parts if not p.get("thought"))
            if not text.strip():
                text = parts[-1].get("text", "")
            m = re.search(r"\{.*\}", text, re.DOTALL)
            parsed = json.loads(m.group(0) if m else text)
            if not isinstance(parsed, dict) or "scores" not in parsed:
                raise ValueError("Missing 'scores' in Gemini JSON response")
            time.sleep(0.3)
            return parsed
        except (urllib.error.HTTPError, urllib.error.URLError, TimeoutError, ValueError, KeyError, json.JSONDecodeError) as exc:
            last_err = exc
            if isinstance(exc, urllib.error.HTTPError):
                if exc.code == 429:
                    err_body = exc.read().decode("utf-8", errors="ignore")
                    if "PerDay" in err_body or "GenerateRequestsPerDay" in err_body:
                        raise RuntimeError(f"Daily free-tier quota exceeded on {model_name}: {err_body[:300]}") from exc
                    time.sleep(62)
                    continue
                if exc.code not in (500, 502, 503, 504):
                    raise
            time.sleep(min(30, 2 ** attempt))

    raise RuntimeError(f"Gemini API call failed after {max_retries} attempts: {last_err}")


def load_completed_keys(csv_path: str) -> set[tuple[str, str, int]]:
    """Load already-scored (record_id, evaluation_mode, run_idx) keys for resumability."""
    path = Path(csv_path)
    if not path.exists():
        return set()
    done: set[tuple[str, str, int]] = set()
    with path.open("r", encoding="utf-8", newline="") as fh:
        reader = csv.DictReader(fh)
        for row in reader:
            try:
                done.add((row["record_id"], row["evaluation_mode"], int(row["run_idx"])))
            except (KeyError, ValueError):
                continue
    return done


def _format_packet_prompt(packet: dict[str, Any]) -> str:
    t0 = packet.get("t0_payload") or {}
    parts = [f"STARTUP OFFERING PACKET (T0)\n\nPitch & Memo:\n{t0.get('pitch_text', '')}"]
    if t0.get("financials"):
        parts.append(f"T0 Financials:\n{json.dumps(t0['financials'], ensure_ascii=False)}")
    if packet.get("social_cue"):
        parts.append(f"Investor Note:\n{packet['social_cue']}")
    return "\n\n".join(parts)


def run_experiment(
    jsonl_paths: list[str],
    output_csv: str,
    n_runs: int = 3,
    temperature: float = 0.2,
    limit: int | None = None,
    smart_design: bool = False,
) -> None:
    """Run the 4-condition Gemini experiment across input JSONLs with row-level resume."""
    records: list[dict[str, Any]] = []
    for path_str in jsonl_paths:
        p = Path(path_str)
        if not p.exists():
            continue
        with p.open("r", encoding="utf-8") as fh:
            for line in fh:
                if line.strip():
                    records.append(json.loads(line))
    if limit is not None:
        records = records[:limit]

    out_path = Path(output_csv)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    completed = load_completed_keys(str(out_path))
    write_header = not out_path.exists() or out_path.stat().st_size == 0

    t1_ids = [r["record_id"] for r in records if r.get("track") == "track1_sec"]
    t2_ids = [r["record_id"] for r in records if r.get("track") == "track2_yc"]
    ablation_ids = set(t2_ids) | set(t1_ids[:40])
    reliability_ids = set(t1_ids[:10]) | set(t2_ids[:10])

    tasks: list[tuple[str, str, str, int, str]] = []
    for rec in records:
        rid = rec["record_id"]
        track = rec.get("track", "unknown")
        modes = EVALUATION_MODES if (not smart_design or rid in ablation_ids) else ["blinded_T0"]
        for mode in modes:
            packet = blind_payload(rec, mode)
            prompt = _format_packet_prompt(packet)
            runs_for_item = n_runs if (not smart_design or (mode == "blinded_T0" and rid in reliability_ids)) else 1
            for run_idx in range(1, runs_for_item + 1):
                if (rid, mode, run_idx) not in completed:
                    tasks.append((rid, track, mode, run_idx, prompt))

    if not tasks:
        return

    write_lock = threading.Lock()
    with out_path.open("a", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=CSV_COLUMNS)
        if write_header:
            writer.writeheader()
            fh.flush()

        def _worker(item: tuple[str, str, str, int, str]) -> dict[str, Any]:
            rid, track, mode, run_idx, prompt = item
            res = call_gemini_json(prompt, temperature=temperature)
            scores = res.get("scores") or {}
            row: dict[str, Any] = {
                "record_id": rid,
                "track": track,
                "evaluation_mode": mode,
                "run_idx": run_idx,
                "composite_score": res.get("composite_score"),
                "predicted_invest": res.get("predicted_invest"),
                "predicted_invest_prob": res.get("predicted_invest_prob"),
                "predicted_survival_prob": res.get("predicted_survival_prob"),
                "confidence": res.get("confidence"),
                "key_risk_flag": res.get("key_risk_flag", ""),
            }
            for dim in RUBRIC_DIMENSIONS:
                row[dim] = scores.get(dim)
            return row

        with concurrent.futures.ThreadPoolExecutor(max_workers=1) as pool:
            for row in pool.map(_worker, tasks):
                with write_lock:
                    writer.writerow(row)
                    fh.flush()
                    completed.add((row["record_id"], row["evaluation_mode"], int(row["run_idx"])))


def main() -> None:
    parser = argparse.ArgumentParser(description="Run 4-condition Gemini startup evaluation experiment.")
    parser.add_argument(
        "--inputs",
        nargs="+",
        default=[
            "data/processed/track1_sec_form_c.jsonl",
            "data/processed/track2_yc_tier_a.jsonl",
        ],
    )
    parser.add_argument("--output", default="results/llm_scores_raw.csv")
    parser.add_argument("--n-runs", type=int, default=3)
    parser.add_argument("--temperature", type=float, default=0.2)
    parser.add_argument("--limit", type=int, default=None)
    parser.add_argument("--smart-design", action="store_true")
    args = parser.parse_args()
    run_experiment(
        args.inputs,
        args.output,
        n_runs=args.n_runs,
        temperature=args.temperature,
        limit=args.limit,
        smart_design=args.smart_design,
    )
    print(f"Experiment complete -> {args.output}")


if __name__ == "__main__":
    main()
