from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any

from src.common import blind_payload

LEAKAGE_PATTERNS: list[tuple[str, re.Pattern[str]]] = [
    ("we were acquired by", re.compile(r"\bwe\s+were\s+acquired\s+by\b", re.IGNORECASE)),
    ("shut down in/our", re.compile(r"\bshut\s+down\s+(?:in\s+20\d\d|our\s+(?:company|startup|business))\b", re.IGNORECASE)),
    ("filed for bankruptcy", re.compile(r"\bfiled\s+for\s+bankruptcy\b", re.IGNORECASE)),
    ("ceased operations in/on", re.compile(r"\bceased\s+operations\s+(?:in|on)\b", re.IGNORECASE)),
    ("went public in/on", re.compile(r"\bwent\s+public\s+(?:in|on)\b", re.IGNORECASE)),
    ("raised Series round", re.compile(r"\braised\s+series\s+[a-z]\b", re.IGNORECASE)),
]

URL_RE = re.compile(r"(?:https?://|www\.)\S+", re.IGNORECASE)


def audit_record(record: dict[str, Any]) -> list[str]:
    """Return a list of T0 leakage or blinding failure strings for a record."""
    issues: list[str] = []
    pitch_text = str((record.get("t0_payload") or {}).get("pitch_text") or "")
    if not pitch_text.strip():
        issues.append("Empty pitch_text in t0_payload.")
        return issues

    for label, pat in LEAKAGE_PATTERNS:
        if pat.search(pitch_text):
            issues.append(f"Post-T0 leakage pattern matched: {label}")

    blinded = blind_payload(record, "blinded_T0")
    blinded_text = str((blinded.get("t0_payload") or {}).get("pitch_text") or "")

    if URL_RE.search(blinded_text):
        issues.append("Unmasked URL remaining after blinding.")

    entities = (record.get("meta") or {}).get("blinding_entities") or {}
    for key in ("company_aliases", "founder_names", "portal_names", "product_terms"):
        for term in entities.get(key) or []:
            if not isinstance(term, str):
                continue
            cleaned = term.strip()
            if len(cleaned) < 3:
                continue
            if re.search(rf"(?<!\w){re.escape(cleaned)}(?!\w)", blinded_text, re.IGNORECASE):
                issues.append(f"Unmasked {key} entity remaining after blinding: {cleaned}")

    return issues


def run_audit(jsonl_paths: list[str], report_path: str) -> bool:
    """Audit all JSONL files and write firewall_audit_report.json. Return True if 0 violations."""
    violations: list[dict[str, Any]] = []
    total_records = 0

    for path_str in jsonl_paths:
        p = Path(path_str)
        if not p.exists():
            continue
        with p.open("r", encoding="utf-8") as fh:
            for line in fh:
                if not line.strip():
                    continue
                total_records += 1
                rec = json.loads(line)
                issues = audit_record(rec)
                if issues:
                    violations.append(
                        {
                            "record_id": rec.get("record_id"),
                            "track": rec.get("track"),
                            "file": str(p),
                            "issues": issues,
                        }
                    )

    report = {
        "total_records": total_records,
        "passed_records": total_records - len(violations),
        "failed_records": len(violations),
        "violations": violations,
    }
    out_p = Path(report_path)
    out_p.parent.mkdir(parents=True, exist_ok=True)
    out_p.write_text(json.dumps(report, indent=2), encoding="utf-8")
    return len(violations) == 0


def main() -> None:
    parser = argparse.ArgumentParser(description="Audit Track 1 and Track 2 JSONLs for T0 leakage and blinding.")
    parser.add_argument(
        "--inputs",
        nargs="+",
        default=[
            "data/processed/track1_sec_form_c.jsonl",
            "data/processed/track2_yc_tier_a.jsonl",
        ],
    )
    parser.add_argument("--report", default="data/processed/firewall_audit_report.json")
    args = parser.parse_args()
    ok = run_audit(args.inputs, args.report)
    print(f"Firewall audit complete -> {args.report} (passed={ok})")
    if not ok:
        sys.exit(1)


if __name__ == "__main__":
    main()
