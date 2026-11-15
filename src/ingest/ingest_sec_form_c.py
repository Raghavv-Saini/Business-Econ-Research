"""Track 1: SEC EDGAR Regulation Crowdfunding (Form C) crawler and two-stage outcome coder."""

from __future__ import annotations

import argparse
import csv
import datetime as dt
import io
import json
import os
import random
import re
import ssl
import time
import urllib.error
import urllib.request
import zipfile
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

from pypdf import PdfReader

from src.common import build_company_aliases

SEC_UA = "BEResearchProject researcher@university.edu"
GEN_UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36"
CTX = ssl.create_default_context()

BASELINE_QUARTERS = [
    f"{y}q{q}" for y in (2018, 2019, 2020) for q in (1, 2, 3, 4)
]
LONGITUDINAL_QUARTERS = [
    f"{y}q{q}"
    for y in range(2018, 2027)
    for q in (1, 2, 3, 4)
    if not (y == 2026 and q == 4)
]


def _sec_get(url: str, timeout: int = 25, sleep_s: float = 0.22) -> bytes:
    last_err: Exception | None = None
    for attempt in range(4):
        time.sleep(sleep_s * (attempt + 1))
        req = urllib.request.Request(url, headers={"User-Agent": SEC_UA})
        try:
            with urllib.request.urlopen(req, timeout=timeout, context=CTX) as resp:
                return resp.read()
        except Exception as exc:
            last_err = exc
    raise RuntimeError(f"Failed SEC GET {url}: {last_err}")


def parse_cu_amount_raised(xml_text: str) -> float | None:
    """Extract dollar amount raised from a Form C-U XML document."""
    if not xml_text:
        return None
    for tag in ("amountRaised", "totalAmountRaised", "dollarAmountRaised", "currentAmountRaised"):
        m = re.search(rf"<(?:\w+:)?{tag}[^>]*>\s*\$?([\d,]+(?:\.\d+)?)\s*</", xml_text, re.I)
        if m:
            try:
                return float(m.group(1).replace(",", ""))
            except ValueError:
                pass
    return None


def parse_ctr_is_failure(xml_text: str) -> bool | None:
    """Return True if Form C-TR indicates cessation/dissolution, False if growth/acquisition, else None."""
    if not xml_text:
        return None
    low = xml_text.lower()
    if re.search(r"<(?:\w+:)?over25millionassets[^>]*>\s*(?:true|1|y|yes)\s*</", low):
        return False
    if re.search(r"<(?:\w+:)?fewerthan300holders[^>]*>\s*(?:true|1|y|yes)\s*</", low):
        return False
    if any(k in low for k in ("acquired", "acquisition", "merger", "ipo", "registered under", "assets exceed")):
        return False
    if re.search(r"<(?:\w+:)?dissolved[^>]*>\s*(?:true|1|y|yes)\s*</", low):
        return True
    if any(k in low for k in ("ceased", "dissolved", "dissolution", "liquidat", "bankrupt", "out of business", "shut down", "winding down")):
        return True
    return None


def _parse_date(val: str) -> dt.date | None:
    s = re.sub(r"[^0-9]", "", str(val or ""))
    if len(s) >= 8:
        try:
            return dt.date(int(s[:4]), int(s[4:6]), int(s[6:8]))
        except ValueError:
            return None
    return None


def code_issuer_outcomes(
    submissions: list[dict[str, Any]],
    c_tr_flags: dict[str, bool | None],
    has_form_d_post: bool,
    website_alive: bool,
) -> dict[str, Any]:
    """Code Stage 1 (funded_outcome) and Stage 2 (survival_3y_outcome, winner_breakout_outcome)."""
    c_dates = [_parse_date(s.get("date", "")) for s in submissions if s.get("type") == "C"]
    c_dates = [d for d in c_dates if d is not None]
    t0_date = min(c_dates) if c_dates else None

    c_ar_dates = [_parse_date(s.get("date", "")) for s in submissions if s.get("type") in ("C-AR", "C-AR/A")]
    c_ar_dates = [d for d in c_ar_dates if d is not None]
    has_cw = any(s.get("type") == "C-W" for s in submissions)
    has_cu = any(s.get("type") in ("C-U", "C-U/A") for s in submissions)

    if c_ar_dates:
        funded = 1
    elif has_cw:
        funded = 0
    elif has_cu:
        funded = 1
    else:
        funded = 0

    if funded == 0:
        return {
            "funded_outcome": 0,
            "survival_3y_outcome": None,
            "winner_breakout_outcome": 1 if has_form_d_post else 0,
            "survival_source": "unfunded_stage1",
        }

    # Stage 2: funded issuers
    ctr_vals = list(c_tr_flags.values())
    has_ctr_exit = any(v is False for v in ctr_vals)
    has_ctr_fail = any(v is True for v in ctr_vals)

    max_car_days = 0
    if t0_date and c_ar_dates:
        max_car_days = max((d - t0_date).days for d in c_ar_dates)

    if has_ctr_exit:
        surv = 1
        src = "ctr_exit_or_threshold"
    elif max_car_days >= 1095:
        surv = 1
        src = "car_3y_plus"
    elif has_form_d_post:
        surv = 1
        src = "delinquency_rescued_form_d"
    elif website_alive and not has_ctr_fail:
        surv = 1
        src = "delinquency_rescued_website"
    elif has_ctr_fail:
        surv = 0
        src = "ctr_dissolution"
    else:
        surv = 0
        src = "car_ceased_and_inactive"

    breakout = 1 if (has_form_d_post or has_ctr_exit) else 0
    return {
        "funded_outcome": 1,
        "survival_3y_outcome": surv,
        "winner_breakout_outcome": breakout,
        "survival_source": src,
    }


def _check_website_alive(url: str) -> bool:
    if not url or not url.strip():
        return False
    u = url.strip()
    if not u.lower().startswith(("http://", "https://")):
        u = "https://" + u
    req = urllib.request.Request(u, headers={"User-Agent": GEN_UA})
    try:
        with urllib.request.urlopen(req, timeout=6, context=CTX) as resp:
            body = resp.read(20000).decode("utf-8", errors="ignore").lower()
            parked_markers = ("domain for sale", "buy this domain", "godaddy", "sedoparking", "hugedomains")
            return resp.status < 400 and not any(m in body for m in parked_markers)
    except Exception:
        return False


def _read_tsv_from_zip(zf: zipfile.ZipFile, suffix: str) -> list[dict[str, str]]:
    match = next((n for n in zf.namelist() if n.upper().endswith(suffix.upper())), None)
    if not match:
        return []
    text = zf.read(match).decode("utf-8", errors="replace")
    return list(csv.DictReader(io.StringIO(text), delimiter="\t"))


def _safe_float(val: Any) -> float | None:
    try:
        s = str(val or "").strip()
        return float(s) if s != "" else None
    except ValueError:
        return None


def _extract_memo_text(cik: str, acc: str, raw_dir: Path) -> str | None:
    acc_nodash = acc.replace("-", "")
    cik_int = str(int(cik))
    memo_cache = raw_dir / "memos" / f"{acc_nodash}.txt"
    if memo_cache.exists():
        return memo_cache.read_text(encoding="utf-8", errors="replace")

    idx_url = f"https://www.sec.gov/Archives/edgar/data/{cik_int}/{acc_nodash}/index.json"
    try:
        idx = json.loads(_sec_get(idx_url, sleep_s=0.18).decode("utf-8"))
    except Exception:
        return None

    items = [it["name"] for it in idx.get("directory", {}).get("item", [])]
    pdfs = [n for n in items if n.lower().endswith(".pdf")]
    # Prefer offering memo PDFs
    pdfs.sort(key=lambda n: (0 if ("memo" in n.lower() or "formc" in n.lower() or "offer" in n.lower()) else 1, n))

    extracted = ""
    for pdf_name in pdfs[:2]:
        pdf_url = f"https://www.sec.gov/Archives/edgar/data/{cik_int}/{acc_nodash}/{pdf_name}"
        try:
            pdf_bytes = _sec_get(pdf_url, timeout=30, sleep_s=0.18)
            reader = PdfReader(io.BytesIO(pdf_bytes))
            pages = [p.extract_text() or "" for p in reader.pages[:25]]
            cand = re.sub(r"\s+", " ", "\n".join(pages)).strip()
            if len(cand.split()) > len(extracted.split()):
                extracted = cand
            if len(extracted.split()) >= 500:
                break
        except Exception:
            continue

    if len(extracted.split()) < 400:
        return None

    memo_cache.parent.mkdir(parents=True, exist_ok=True)
    capped = extracted[:18000]
    memo_cache.write_text(capped, encoding="utf-8")
    return capped


def run_ingestion(repo_root: Path, target_n: int = 165, seed: int = 42) -> None:
    raw_dir = repo_root / "data" / "raw" / "sec"
    zip_dir = raw_dir / "zips"
    zip_dir.mkdir(parents=True, exist_ok=True)
    proc_dir = repo_root / "data" / "processed"
    proc_dir.mkdir(parents=True, exist_ok=True)

    all_subs_by_cik: dict[str, list[dict[str, Any]]] = defaultdict(list)
    baseline_c: dict[str, dict[str, Any]] = {}
    issuer_info: dict[str, dict[str, str]] = {}
    disclosures: dict[str, dict[str, str]] = {}
    signatures: dict[str, list[str]] = defaultdict(list)

    for q in LONGITUDINAL_QUARTERS:
        zp = zip_dir / f"{q}_cf.zip"
        if not zp.exists():
            url = f"https://www.sec.gov/files/dera/data/crowdfunding-offerings-data-sets/{q}_cf.zip"
            try:
                zp.write_bytes(_sec_get(url, timeout=45, sleep_s=0.25))
            except Exception as exc:
                print(f"Skipping missing quarter {q}: {exc}")
                continue
        with zipfile.ZipFile(zp, "r") as zf:
            for row in _read_tsv_from_zip(zf, "FORM_C_SUBMISSION.tsv"):
                cik = row.get("CIK", "").strip()
                acc = row.get("ACCESSION_NUMBER", "").strip()
                stype = row.get("SUBMISSION_TYPE", "").strip()
                fdate = row.get("FILING_DATE", "").strip()
                if not cik or not acc:
                    continue
                all_subs_by_cik[cik].append({"acc": acc, "type": stype, "date": fdate})
                if q in BASELINE_QUARTERS and stype == "C":
                    prev = baseline_c.get(cik)
                    if prev is None or fdate < prev["date"]:
                        baseline_c[cik] = {"cik": cik, "acc": acc, "date": fdate, "quarter": q}
            if q in BASELINE_QUARTERS:
                for row in _read_tsv_from_zip(zf, "FORM_C_ISSUER_INFORMATION.tsv"):
                    acc = row.get("ACCESSION_NUMBER", "").strip()
                    if acc:
                        issuer_info[acc] = row
                for row in _read_tsv_from_zip(zf, "FORM_C_DISCLOSURE.tsv"):
                    acc = row.get("ACCESSION_NUMBER", "").strip()
                    if acc:
                        disclosures[acc] = row
                for row in _read_tsv_from_zip(zf, "FORM_C_SIGNATURE.tsv"):
                    acc = row.get("ACCESSION_NUMBER", "").strip()
                    sig = row.get("PERSONSIGNATURE", "").strip()
                    if acc and sig:
                        signatures[acc].append(sig)

    # Preliminary population stratification across all baseline 2018-2020 CIKs
    strata: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for cik, base in baseline_c.items():
        acc = base["acc"]
        disc = disclosures.get(acc, {})
        info = issuer_info.get(acc, {})
        if not disc or not info or _safe_float(disc.get("OFFERINGAMOUNT")) is None:
            continue
        subs = all_subs_by_cik[cik]
        t0_d = _parse_date(base["date"])
        car_dates = [_parse_date(s["date"]) for s in subs if s["type"] in ("C-AR", "C-AR/A")]
        car_dates = [d for d in car_dates if d is not None]
        has_cw = any(s["type"] == "C-W" for s in subs)
        has_cu = any(s["type"] in ("C-U", "C-U/A") for s in subs)
        if not car_dates and (has_cw or not has_cu):
            cell = "unfunded_prelim"
        elif t0_d and car_dates and max((d - t0_d).days for d in car_dates) >= 1095:
            cell = "funded_survived_prelim"
        else:
            cell = "funded_failed_or_delinquent_prelim"
        strata[cell].append(base)

    pop_counts = {k: len(v) for k, v in strata.items()}
    pop_counts["total_eligible_baseline_ciks"] = sum(pop_counts.values())
    (proc_dir / "sec_population_counts.json").write_text(json.dumps(pop_counts, indent=2), encoding="utf-8")
    print("SEC 2018-2020 Population Counts:", pop_counts)

    rng = random.Random(seed)
    per_cell_target = max(1, target_n // 3)
    per_cell_buffer = per_cell_target + 35

    records: list[dict[str, Any]] = []
    for cell_name, items in strata.items():
        pool = list(items)
        rng.shuffle(pool)
        kept = 0
        for base in pool[: per_cell_buffer * 2]:
            if kept >= per_cell_target:
                break
            cik = base["cik"]
            acc = base["acc"]
            info = issuer_info[acc]
            disc = disclosures[acc]

            memo_text = _extract_memo_text(cik, acc, raw_dir)
            if not memo_text:
                continue

            # Fetch EDGAR submissions JSON for longitudinal Form D + C-U / C-TR XMLs
            cik_pad = cik.zfill(10)
            has_form_d_post = False
            c_tr_flags: dict[str, bool | None] = {}
            cu_amounts: list[float] = []

            try:
                sub_json = json.loads(
                    _sec_get(f"https://data.sec.gov/submissions/CIK{cik_pad}.json", sleep_s=0.18).decode("utf-8")
                )
                recent = sub_json.get("filings", {}).get("recent", {})
                forms = recent.get("form", [])
                fdates = recent.get("filingDate", [])
                accs = recent.get("accessionNumber", [])
                pdocs = recent.get("primaryDocument", [])
                t0_str = f"{base['date'][:4]}-{base['date'][4:6]}-{base['date'][6:8]}"
                for frm, fdt, facc, pdoc in zip(forms, fdates, accs, pdocs):
                    if frm in ("D", "D/A") and fdt > t0_str:
                        has_form_d_post = True
                    elif frm in ("C-U", "C-U/A") and pdoc:
                        try:
                            xml_b = _sec_get(
                                f"https://www.sec.gov/Archives/edgar/data/{int(cik)}/{facc.replace('-','')}/{pdoc}",
                                sleep_s=0.15,
                            ).decode("utf-8", errors="replace")
                            amt = parse_cu_amount_raised(xml_b)
                            if amt is not None:
                                cu_amounts.append(amt)
                        except Exception:
                            pass
                    elif frm in ("C-TR", "C-TR/A") and pdoc:
                        try:
                            xml_b = _sec_get(
                                f"https://www.sec.gov/Archives/edgar/data/{int(cik)}/{facc.replace('-','')}/{pdoc}",
                                sleep_s=0.15,
                            ).decode("utf-8", errors="replace")
                            c_tr_flags[facc] = parse_ctr_is_failure(xml_b)
                        except Exception:
                            c_tr_flags[facc] = None
            except Exception:
                pass

            website = info.get("ISSUERWEBSITE", "").strip()
            website_alive = _check_website_alive(website) if cell_name == "funded_failed_or_delinquent_prelim" else False
            outcomes = code_issuer_outcomes(all_subs_by_cik[cik], c_tr_flags, has_form_d_post, website_alive)

            off_amt = _safe_float(disc.get("OFFERINGAMOUNT")) or 0.0
            max_raised = max(cu_amounts) if cu_amounts else None
            funding_ratio = (max_raised / off_amt) if (max_raised is not None and off_amt > 0) else (1.0 if outcomes["funded_outcome"] == 1 else 0.0)
            outcomes["amount_raised"] = max_raised
            outcomes["funding_ratio"] = round(funding_ratio, 4)

            legal_name = info.get("NAMEOFISSUER", "").strip()
            portal_name = info.get("COMPANYNAME", "").strip()
            aliases = build_company_aliases(legal_name)
            founders = sorted(set(signatures.get(acc, [])))

            financials = {
                "offering_amount": off_amt,
                "max_offering_amount": _safe_float(disc.get("MAXIMUMOFFERINGAMOUNT")),
                "security_type": disc.get("SECURITYOFFEREDTYPE", "").strip(),
                "employees": _safe_float(disc.get("CURRENTEMPLOYEES")),
                "assets_recent": _safe_float(disc.get("TOTALASSETMOSTRECENTFISCALYEAR")),
                "cash_recent": _safe_float(disc.get("CASHEQUIMOSTRECENTFISCALYEAR")),
                "short_term_debt_recent": _safe_float(disc.get("SHORTTERMDEBTMRECENTFISCALYEAR")),
                "long_term_debt_recent": _safe_float(disc.get("LONGTERMDEBTRECENTFISCALYEAR")),
                "revenue_recent": _safe_float(disc.get("REVENUEMOSTRECENTFISCALYEAR")),
                "net_income_recent": _safe_float(disc.get("NETINCOMEMOSTRECENTFISCALYEAR")),
            }

            rec = {
                "record_id": f"SEC-{cik}",
                "track": "track1_sec",
                "meta": {
                    "cik": cik,
                    "accession_number": acc,
                    "filing_date": base["date"],
                    "quarter": base["quarter"],
                    "prelim_stratum": cell_name,
                    "issuer_website": website,
                    "blinding_entities": {
                        "company_aliases": aliases,
                        "founder_names": founders,
                        "portal_names": [portal_name] if portal_name else [],
                        "product_terms": [],
                    },
                },
                "t0_payload": {
                    "pitch_text": memo_text,
                    "financials": financials,
                },
                "outcomes": outcomes,
            }
            records.append(rec)
            kept += 1
            print(f"[{len(records)}] {rec['record_id']} ({legal_name[:30]}) -> funded={outcomes['funded_outcome']}, surv={outcomes['survival_3y_outcome']} ({outcomes['survival_source']})")

    out_jsonl = proc_dir / "track1_sec_form_c.jsonl"
    with out_jsonl.open("w", encoding="utf-8") as f:
        for r in records:
            f.write(json.dumps(r) + "\n")

    # Export 20-record random audit CSV
    audit_sample = rng.sample(records, min(20, len(records)))
    audit_csv = proc_dir / "track1_audit_sample_20.csv"
    with audit_csv.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(
            f,
            fieldnames=["record_id", "company_name", "filing_date", "issuer_website", "funded_outcome", "survival_3y_outcome", "winner_breakout_outcome", "survival_source", "amount_raised", "funding_ratio"],
        )
        w.writeheader()
        for r in audit_sample:
            w.writerow({
                "record_id": r["record_id"],
                "company_name": r["meta"]["blinding_entities"]["company_aliases"][0],
                "filing_date": r["meta"]["filing_date"],
                "issuer_website": r["meta"]["issuer_website"],
                "funded_outcome": r["outcomes"]["funded_outcome"],
                "survival_3y_outcome": r["outcomes"]["survival_3y_outcome"],
                "winner_breakout_outcome": r["outcomes"]["winner_breakout_outcome"],
                "survival_source": r["outcomes"]["survival_source"],
                "amount_raised": r["outcomes"]["amount_raised"],
                "funding_ratio": r["outcomes"]["funding_ratio"],
            })
    print(f"Wrote {len(records)} Track 1 records to {out_jsonl} and {len(audit_sample)} audit rows to {audit_csv}.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--target-n", type=int, default=165)
    parser.add_argument("--seed", type=int, default=42)
    args = parser.parse_args()
    run_ingestion(Path(__file__).resolve().parents[2], target_n=args.target_n, seed=args.seed)
