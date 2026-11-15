from __future__ import annotations

import argparse
import io
import json
import re
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Any

from bs4 import BeautifulSoup
from pypdf import PdfReader

from src.common import build_company_aliases

DEFAULT_QUEUE_PATH = Path(r"c:\Users\meetp\Desktop\BE\option_b_tier_a_queue_21_v2.jsonl")
USER_AGENT = "BusinessEconResearchBot/1.0 (academic-research; contact: research@example.edu)"

URL_OVERRIDES: dict[str, str] = {
    "OPTB-002": "https://about.gitlab.com/2016/09/30/gitlabs-application-for-y-combinator-winter-2015/",
}
EXCLUDED_NON_T0_IDS: set[str] = {"OPTB-003", "OPTB-004", "OPTB-008", "OPTB-015"}

VERIFIED_EXTRA_APPS: list[dict[str, Any]] = [
    {
        "record_id": "OPTB-EXT-01",
        "meta": {
            "provenance_tier": "Tier-A",
            "provenance_note": "Verbatim Application (MakersClaw)",
            "source_url": "https://makersclaw.com/blog/familyleaf-yc-application-w12",
            "t0_text_status": "pending_text_ingestion",
            "accelerator_decision": 1,
            "three_year_outcome": 1,
            "blinding_entities": {
                "company_aliases": ["FamilyLeaf"],
                "founder_names": ["Wes Bos", "Ajay Mehta"],
                "product_terms": ["FamilyLeaf"],
            },
        },
        "blended_pitch_text": {"batch_cycle": "YC W12"},
    },
    {
        "record_id": "OPTB-EXT-02",
        "meta": {
            "provenance_tier": "Tier-A",
            "provenance_note": "Verbatim Application (MakersClaw)",
            "source_url": "https://makersclaw.com/blog/80000-hours-yc-application-s15",
            "t0_text_status": "pending_text_ingestion",
            "accelerator_decision": 1,
            "three_year_outcome": 1,
            "blinding_entities": {
                "company_aliases": ["80,000 Hours", "80000 Hours"],
                "founder_names": ["Benjamin Todd", "William MacAskill"],
                "product_terms": ["80,000 Hours"],
            },
        },
        "blended_pitch_text": {"batch_cycle": "YC S15"},
    },
    {
        "record_id": "OPTB-EXT-03",
        "meta": {
            "provenance_tier": "Tier-A",
            "provenance_note": "Verbatim Application (MakersClaw)",
            "source_url": "https://makersclaw.com/blog/simple-habit-yc-application-w17",
            "t0_text_status": "pending_text_ingestion",
            "accelerator_decision": 1,
            "three_year_outcome": 1,
            "blinding_entities": {
                "company_aliases": ["Simple Habit"],
                "founder_names": ["Yunha Kim"],
                "product_terms": ["Simple Habit"],
            },
        },
        "blended_pitch_text": {"batch_cycle": "YC W17"},
    },
    {
        "record_id": "OPTB-EXT-04",
        "meta": {
            "provenance_tier": "Tier-A",
            "provenance_note": "Verbatim Application (MakersClaw)",
            "source_url": "https://makersclaw.com/blog/slite-yc-application-w18",
            "t0_text_status": "pending_text_ingestion",
            "accelerator_decision": 1,
            "three_year_outcome": 1,
            "blinding_entities": {
                "company_aliases": ["Slite"],
                "founder_names": ["Christophe Pasquier"],
                "product_terms": ["Slite"],
            },
        },
        "blended_pitch_text": {"batch_cycle": "YC W18"},
    },
    {
        "record_id": "OPTB-EXT-05",
        "meta": {
            "provenance_tier": "Tier-A",
            "provenance_note": "Verbatim Application (MakersClaw)",
            "source_url": "https://makersclaw.com/blog/dendron-yc-application-w21",
            "t0_text_status": "pending_text_ingestion",
            "accelerator_decision": 1,
            "three_year_outcome": 1,
            "blinding_entities": {
                "company_aliases": ["Dendron"],
                "founder_names": ["Kevin Lin"],
                "product_terms": ["Dendron"],
            },
        },
        "blended_pitch_text": {"batch_cycle": "YC W21"},
    },
]


_QA_START_RE = re.compile(
    r"(?:Company name:|Describe what your company|What is your company going to make|Please tell us in one or two sentences|What are you going to make)",
    re.IGNORECASE,
)


def strip_post_t0_wrappers(text: str, source_url: str = "") -> str:
    """Remove Wayback toolbar chrome, blog bylines, and retrospective intros before YC Q&A."""
    cleaned = re.sub(r"^.*?\bAbout this capture\b\s*", "", text, flags=re.IGNORECASE)
    cleaned = re.sub(r"\bUpdated\s+\d{1,2}/\d{1,2}/20\d\d\b", "", cleaned, flags=re.IGNORECASE)
    if "makersclaw.com" in source_url.lower() or len(cleaned) > 1200:
        m = _QA_START_RE.search(cleaned)
        if m and m.start() > 0:
            cleaned = cleaned[m.start():]
    cleaned = re.sub(r"\s*(?:©|Copyright)\s*20\d\d.*$", "", cleaned, flags=re.IGNORECASE)
    cleaned = re.sub(r"\s*(?:Read the blog|Related\s+posts?|Published\s+\d{1,2}\s+[A-Za-z]+\s+20\d\d).*$", "", cleaned, flags=re.IGNORECASE)
    return re.sub(r"\s+", " ", cleaned).strip()


def extract_clean_text_from_html(html: str) -> str:
    """Strip boilerplate HTML tags and return normalized prose text."""
    soup = BeautifulSoup(html, "html.parser")
    for tag in soup(["script", "style", "nav", "header", "footer", "aside", "noscript", "svg"]):
        tag.decompose()
    for wb_id in ("wm-ipp-base", "wm-ipp", "donato"):
        wb = soup.find(id=wb_id)
        if wb:
            wb.decompose()
    main = soup.find("article") or soup.find("main") or soup.body or soup
    text = main.get_text(separator=" ", strip=True)
    return re.sub(r"\s+", " ", text).strip()


def _parse_batch_year(batch_cycle: str | None) -> int | None:
    if not batch_cycle:
        return None
    m = re.search(r"\b(?:S|W|F)(\d{2})\b", batch_cycle)
    if m:
        yr = int(m.group(1))
        return 2000 + yr if yr < 50 else 1900 + yr
    if "Fellowship" in batch_cycle:
        return 2015
    return None


def _compose_populated_pitch(blended: dict[str, Any]) -> str:
    sections = [
        ("One-liner & Product", blended.get("one_liner_and_product")),
        ("Problem & Target User", blended.get("problem_and_target_user")),
        ("Traction & Metrics (T0)", blended.get("traction_and_metrics_t0")),
        ("Team & Domain Expertise", blended.get("team_and_domain_expertise")),
        ("Insight & Differentiation", blended.get("insight_and_differentiation")),
        ("Monetization & Market", blended.get("monetization_and_market")),
    ]
    parts = [f"{label}: {val.strip()}" for label, val in sections if isinstance(val, str) and val.strip()]
    return "\n".join(parts)


def build_track2_record(
    raw_rec: dict[str, Any],
    harvested_text: str | None,
    yc_oss_status: str | None,
) -> dict[str, Any] | None:
    """Build a unified Track 2 record, returning None if T0 text is unavailable."""
    meta = dict(raw_rec.get("meta") or {})
    blended = dict(raw_rec.get("blended_pitch_text") or {})
    status = meta.get("t0_text_status")

    if status == "populated_ready":
        pitch_text = _compose_populated_pitch(blended)
    elif harvested_text and len(harvested_text.strip()) >= 200:
        cleaned = strip_post_t0_wrappers(harvested_text, str(meta.get("source_url", "")))
        pitch_text = cleaned[:8000] if len(cleaned) >= 200 else ""
    else:
        return None

    if not pitch_text:
        return None

    batch_cycle = blended.get("batch_cycle")
    t0_year = _parse_batch_year(batch_cycle)

    blinding = dict(meta.get("blinding_entities") or {})
    aliases = list(blinding.get("company_aliases") or [])
    if aliases:
        expanded = build_company_aliases(aliases[0], aliases[1:])
        blinding["company_aliases"] = expanded
    blinding.setdefault("founder_names", [])
    blinding.setdefault("portal_names", [])
    blinding.setdefault("product_terms", [])
    meta["blinding_entities"] = blinding
    meta["batch_cycle"] = batch_cycle
    meta["yc_oss_status"] = yc_oss_status

    accel_dec = meta.get("accelerator_decision")
    surv_3y = meta.get("three_year_outcome")
    if t0_year is not None and t0_year >= 2024:
        surv_3y = None

    if yc_oss_status in {"Active", "Public", "Acquired"}:
        winner_out: int | None = 1
    elif yc_oss_status == "Inactive":
        winner_out = 0
    else:
        winner_out = surv_3y

    return {
        "record_id": raw_rec["record_id"],
        "track": "track2_yc",
        "t0_year": t0_year,
        "meta": meta,
        "t0_payload": {
            "pitch_text": pitch_text,
            "financials": {
                "source": "yc_application",
                "batch_cycle": batch_cycle,
            },
        },
        "outcomes": {
            "funded_outcome": accel_dec,
            "survival_3y_outcome": surv_3y,
            "winner_breakout_outcome": winner_out,
        },
    }


def _http_get_bytes(url: str, timeout: int = 20) -> bytes | None:
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return resp.read()
    except Exception:
        return None


def _wayback_snapshot_url(target_url: str) -> str | None:
    api = "https://archive.org/wayback/available?" + urllib.parse.urlencode({"url": target_url})
    raw = _http_get_bytes(api, timeout=15)
    if not raw:
        return None
    try:
        data = json.loads(raw.decode("utf-8", errors="ignore"))
        closest = data.get("archived_snapshots", {}).get("closest", {})
        if closest.get("available") and closest.get("url"):
            return str(closest["url"])
    except Exception:
        return None
    return None


def _extract_pdf_bytes(data: bytes) -> str:
    try:
        reader = PdfReader(io.BytesIO(data))
        pages = [page.extract_text() or "" for page in reader.pages]
        return re.sub(r"\s+", " ", " ".join(pages)).strip()
    except Exception:
        return ""


def _harvest_url_text(url: str) -> str | None:
    candidates = [url]
    wb = _wayback_snapshot_url(url)
    if wb:
        candidates.append(wb)

    for candidate in candidates:
        raw = _http_get_bytes(candidate, timeout=20)
        if not raw:
            continue
        if candidate.lower().endswith(".pdf") or raw[:4] == b"%PDF":
            txt = _extract_pdf_bytes(raw)
        else:
            txt = extract_clean_text_from_html(raw.decode("utf-8", errors="ignore"))
        if len(txt) >= 200:
            return txt
    return None


def _fetch_yc_oss_statuses() -> dict[str, str]:
    url = "https://yc-oss.github.io/api/companies/all.json"
    raw = _http_get_bytes(url, timeout=25)
    if not raw:
        return {}
    try:
        rows = json.loads(raw.decode("utf-8", errors="ignore"))
        return {
            str(r.get("name", "")).strip().lower(): str(r.get("status", "")).strip()
            for r in rows
            if r.get("name") and r.get("status")
        }
    except Exception:
        return {}


def run_yc_ingestion(repo_root: Path, queue_path: Path = DEFAULT_QUEUE_PATH) -> list[dict[str, Any]]:
    raw_records: list[dict[str, Any]] = []
    if queue_path.exists():
        with queue_path.open("r", encoding="utf-8") as fh:
            for line in fh:
                if line.strip():
                    raw_records.append(json.loads(line))
    raw_records.extend(VERIFIED_EXTRA_APPS)

    yc_statuses = _fetch_yc_oss_statuses()
    out_records: list[dict[str, Any]] = []

    for rec in raw_records:
        rid = rec["record_id"]
        if rid in EXCLUDED_NON_T0_IDS:
            continue
        meta = rec.get("meta") or {}
        aliases = (meta.get("blinding_entities") or {}).get("company_aliases") or []
        yc_status = None
        for alias in aliases:
            if alias.lower() in yc_statuses:
                yc_status = yc_statuses[alias.lower()]
                break

        harvested = None
        if meta.get("t0_text_status") != "populated_ready":
            target_url = URL_OVERRIDES.get(rid, meta.get("source_url", ""))
            if target_url:
                harvested = _harvest_url_text(target_url)

        built = build_track2_record(rec, harvested, yc_status)
        if built is not None:
            out_records.append(built)

    out_path = repo_root / "data" / "processed" / "track2_yc_tier_a.jsonl"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with out_path.open("w", encoding="utf-8") as fh:
        for row in out_records:
            fh.write(json.dumps(row, ensure_ascii=False) + "\n")
    return out_records


def main() -> None:
    parser = argparse.ArgumentParser(description="Harvest Track 2 YC Tier-A T0 applications.")
    parser.add_argument("--repo-root", default=".", help="Repository root directory")
    parser.add_argument("--queue-path", default=str(DEFAULT_QUEUE_PATH), help="Path to option_b_tier_a_queue_21_v2.jsonl")
    args = parser.parse_args()
    records = run_yc_ingestion(Path(args.repo_root).resolve(), Path(args.queue_path))
    print(f"Wrote {len(records)} Track 2 records to data/processed/track2_yc_tier_a.jsonl")


if __name__ == "__main__":
    main()
