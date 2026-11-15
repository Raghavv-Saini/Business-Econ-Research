"""Shared schemas, unified T0 prompt, and entity-blinding helpers."""

from __future__ import annotations

import copy
import re
from typing import Any

RUBRIC_DIMENSIONS: list[str] = [
    "team_and_background",
    "execution_plan",
    "financial_feasibility",
    "writing_and_polish",
    "value_proposition_innovativeness",
    "market_opportunity",
    "competitive_moat",
    "customer_need_alignment",
    "roi_potential",
    "long_run_viability",
]

SOCIAL_CUE_POS = (
    "Note on early campaign reception: Independent early angel diligence was positive, "
    "with strong initial commitments ahead of the main close."
)

SOCIAL_CUE_NEG = (
    "Note on early campaign reception: Early institutional/angel reviewers expressed "
    "skepticism, with slow initial commitments ahead of the main close."
)

UNIFIED_SYSTEM_PROMPT_T0 = """You are an early-stage startup investment analyst evaluating a venture at the exact timestamp of its initial pitch/filing (T0).
STRICT TEMPORAL FIREWALL:
- Evaluate ONLY the provided T0 information packet.
- Do NOT use any post-T0 knowledge, brand recognition, or retrospective outcome information.
- Score each of the 10 dimensions on an integer scale from 0 to 100.
- Provide a binary investment recommendation (`predicted_invest`: 1 = Invest/Fund, 0 = Pass/Reject), an estimated fundraising probability (`predicted_invest_prob`: 0.00 to 1.00), an estimated 3-year survival probability (`predicted_survival_prob`: 0.00 to 1.00), and your overall confidence (`confidence`: 0 to 100).

Return valid JSON matching this exact schema:
{
  "scores": {
    "team_and_background": <0-100>,
    "execution_plan": <0-100>,
    "financial_feasibility": <0-100>,
    "writing_and_polish": <0-100>,
    "value_proposition_innovativeness": <0-100>,
    "market_opportunity": <0-100>,
    "competitive_moat": <0-100>,
    "customer_need_alignment": <0-100>,
    "roi_potential": <0-100>,
    "long_run_viability": <0-100>
  },
  "composite_score": <float 0-100>,
  "predicted_invest": <0 or 1>,
  "predicted_invest_prob": <float 0.0-1.0>,
  "predicted_survival_prob": <float 0.0-1.0>,
  "confidence": <0-100>,
  "key_risk_flag": "<one concise sentence>"
}"""

VALID_MODES = {"blinded_T0", "unblinded_T0", "social_cue_pos", "social_cue_neg"}

_LEGAL_SUFFIX_RE = re.compile(
    r",?\s*\b(?:Incorporated|Corporation|Inc\.?|L\.L\.C\.|LLC|Corp\.?|Ltd\.?|Co\.?|P\.?B\.?C\.?|LP|L\.P\.?|LLP)\s*$",
    re.IGNORECASE,
)

_URL_RE = re.compile(
    r"https?://\S+|www\.\S+|\b[a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)*\.(?:com|io|org|co|ai|net|cz|so|app|dev|xyz)\b",
    re.IGNORECASE,
)


def build_company_aliases(legal_name: str, extra_aliases: list[str] | None = None) -> list[str]:
    """Return deduplicated company aliases including suffix-stripped forms, longest first."""
    candidates: list[str] = []
    for raw in [legal_name, *(extra_aliases or [])]:
        cleaned = (raw or "").strip()
        if not cleaned:
            continue
        candidates.append(cleaned)
        stripped = cleaned
        for _ in range(3):
            next_s = _LEGAL_SUFFIX_RE.sub("", stripped).strip(" ,.")
            if next_s and next_s != stripped:
                candidates.append(next_s)
                stripped = next_s
            else:
                break
    seen: set[str] = set()
    unique: list[str] = []
    for item in sorted(candidates, key=len, reverse=True):
        key = item.lower()
        if len(item) >= 2 and key not in seen:
            seen.add(key)
            unique.append(item)
    return unique


def _mask_text(text: str, rec_id: str, entities: dict[str, list[str]]) -> str:
    if not text:
        return text
    masked = _URL_RE.sub("[URL_REDACTED]", text)
    for alias in sorted(entities.get("company_aliases", []), key=len, reverse=True):
        if alias:
            masked = re.sub(rf"(?<!\w){re.escape(alias)}(?!\w)", f"[{rec_id}_STARTUP]", masked, flags=re.IGNORECASE)
    for idx, fname in enumerate(sorted(entities.get("founder_names", []), key=len, reverse=True), start=1):
        if fname:
            masked = re.sub(rf"(?<!\w){re.escape(fname)}(?!\w)", f"[FOUNDER_{idx}]", masked, flags=re.IGNORECASE)
    for idx, pname in enumerate(sorted(entities.get("portal_names", []), key=len, reverse=True), start=1):
        if pname:
            masked = re.sub(rf"(?<!\w){re.escape(pname)}(?!\w)", f"[PORTAL_{idx}]", masked, flags=re.IGNORECASE)
    for idx, term in enumerate(sorted(entities.get("product_terms", []), key=len, reverse=True), start=1):
        if term:
            masked = re.sub(rf"(?<!\w){re.escape(term)}(?!\w)", f"[PRODUCT_TERM_{idx}]", masked, flags=re.IGNORECASE)
    return masked


def _mask_recursive(obj: Any, rec_id: str, entities: dict[str, list[str]]) -> Any:
    if isinstance(obj, str):
        return _mask_text(obj, rec_id, entities)
    if isinstance(obj, dict):
        return {k: (_mask_recursive(v, rec_id, entities) if k != "financials" else copy.deepcopy(v)) for k, v in obj.items()}
    if isinstance(obj, list):
        return [_mask_recursive(v, rec_id, entities) for v in obj]
    return obj


def blind_payload(record: dict[str, Any], mode: str) -> dict[str, Any]:
    """Prepare the evaluator payload for one of the 4 experimental conditions."""
    if mode not in VALID_MODES:
        raise ValueError(f"Unsupported evaluation mode: {mode!r}")

    rec_id = record["record_id"]
    payload = copy.deepcopy(record["t0_payload"])
    if mode != "unblinded_T0":
        entities = record.get("meta", {}).get("blinding_entities", {})
        payload = _mask_recursive(payload, rec_id, entities)
    if mode == "social_cue_pos":
        payload["social_cue"] = SOCIAL_CUE_POS
    elif mode == "social_cue_neg":
        payload["social_cue"] = SOCIAL_CUE_NEG

    return {
        "record_id": rec_id,
        "track": record.get("track", "unknown"),
        "evaluation_mode": mode,
        "t0_payload": payload,
    }
