# Track 1 + Track 2 Startup Evaluation Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use `superpowers:subagent-driven-development` (recommended) or `superpowers:executing-plans` to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build and execute the dual-track empirical study (SEC EDGAR Form C $N=150$–$200$ + audited YC Tier-A $N \approx 18$–$22$) with a 4-condition Gemini 2.5 Flash evaluation, econometric analysis, and publication-style Business Economics report in Markdown and `.docx`.

**Architecture:** Seven modular Python components under `Business-Econ-Research/src/` and `report/` separate data ingestion/auditing (`ingest_sec_form_c.py`, `ingest_yc_tier_a.py`, `audit_t0_firewall.py`), resumable LLM evaluation (`run_llm_experiment.py`), statistical/econometric analysis (`analyze_results.py`), and `.docx` report generation (`build_docx.py`). Every record passes a strict $T_0$ leakage and entity-blinding gate before touching the Gemini API.

**Tech Stack:** Python 3.14 (`.venv`), `pandas`, `numpy`, `scipy`, `statsmodels`, `scikit-learn`, `matplotlib`, `pypdf`, `beautifulsoup4`, `python-docx`, `pytest`, Gemini REST API (`gemini-2.5-flash`).

**Spec:** [2026-11-15-track1-track2-startup-eval-design.md](file:///c:/Users/meetp/Desktop/BE/Business-Econ-Research/docs/superpowers/specs/2026-11-15-track1-track2-startup-eval-design.md)

## Global Constraints
- Run all Python commands via `c:\Users\meetp\Desktop\BE\Business-Econ-Research\.venv\Scripts\python.exe` (created from `C:\Users\meetp\AppData\Local\Programs\Python\Python314\python.exe`).
- Read `GEMINI_API_KEY` strictly from `os.environ` at runtime; never hardcode, print, or commit keys.
- Use a compliant SEC EDGAR `User-Agent` header (`BEResearchProject researcher@university.edu`) and throttle EDGAR requests to $\le 5$ req/s with exponential backoff on 429/5xx.
- Preserve existing starter files in `c:\Users\meetp\Desktop\BE\` (`option_b_master_register_100_v2.csv`, `option_b_tier_a_queue_21_v2.jsonl`, `option_b_phase2_pipeline_v2.py`) unmodified; write all new code, data, results, and reports inside `c:\Users\meetp\Desktop\BE\Business-Econ-Research\`.
- Zero look-ahead leakage: never pass post-$T_0$ outcomes, `yc-oss` `long_description`s, or post-offering filing text into LLM prompts.

## Review Focus
- **Legal-suffix name leaks in entity blinding:** If `NAMEOFISSUER` is `"Acme Robotics, Inc."`, prose mentioning `"Acme Robotics"` or `"Acme Robotics Inc"` will leak unless suffix-stripped aliases are generated and tested (Task 1).
- **Missing or scanned/image-only `offeringmemoformc.pdf`:** Some SEC Form C PDFs yield `< 400` words of extractable text; `ingest_sec_form_c.py` must filter them out before sampling rather than writing empty payloads (Task 2).
- **`Form C-TR` & `Form C-U` XML variation:** Older/newer Form C XMLs use slightly different tag casing or omit `amount_raised`; parser must handle missing tags gracefully without mislabeling acquisitions as failures (Task 2).
- **Gemini API rate limits / partial run interruption:** A 2,040-call run can hit transient 429/503 errors or be interrupted; `run_llm_experiment.py` must flush each row immediately and resume idempotently on `(record_id, evaluation_mode, run_idx)` (Task 5).
- **Zero-variance or small-cell edge cases in weighted/CV logits:** Outcome-stratified subsets or `Form D` breakout winners can be sparse; `analyze_results.py` must guard against degenerate folds or singular matrices cleanly (Task 6).

---

### Task 1: Environment Setup, Shared Schema, Prompt & Entity-Blinding (`src/common.py`)

**Files:**
- Create: `c:\Users\meetp\Desktop\BE\Business-Econ-Research\requirements.txt`
- Create: `c:\Users\meetp\Desktop\BE\Business-Econ-Research\src\__init__.py`
- Create: `c:\Users\meetp\Desktop\BE\Business-Econ-Research\src\common.py`
- Test: `c:\Users\meetp\Desktop\BE\Business-Econ-Research\tests\test_common.py`

**Interfaces:**
- Produces:
  - `RUBRIC_DIMENSIONS: list[str]` (10 Csaszar dimensions)
  - `UNIFIED_SYSTEM_PROMPT_T0: str`
  - `SOCIAL_CUE_POS: str`, `SOCIAL_CUE_NEG: str`
  - `build_company_aliases(legal_name: str, extra_aliases: list[str] | None = None) -> list[str]`
  - `blind_payload(record: dict, mode: str) -> dict` (`mode` in `{"blinded_T0", "unblinded_T0", "social_cue_pos", "social_cue_neg"}`)

- [ ] **Step 1: Create `.venv` and install pinned dependencies**
  Run `C:\Users\meetp\AppData\Local\Programs\Python\Python314\python.exe -m venv .venv` inside `Business-Econ-Research` and install `pandas numpy scipy statsmodels scikit-learn matplotlib pypdf beautifulsoup4 python-docx pytest` into `.venv`.
  Verify: `.venv\Scripts\python.exe -m pytest --version` prints pytest version.

- [ ] **Step 2: Write the failing tests in `tests/test_common.py`**
```python
from src.common import build_company_aliases, blind_payload, RUBRIC_DIMENSIONS

def test_build_company_aliases_strips_legal_suffixes():
    aliases = build_company_aliases("Acme Robotics, Inc.", ["AcmeBot"])
    assert "Acme Robotics, Inc." in aliases
    assert "Acme Robotics" in aliases
    assert "AcmeBot" in aliases

def test_blind_payload_masks_entities_and_attaches_social_cues():
    rec = {
        "record_id": "SEC-001",
        "track": "track1_sec",
        "meta": {"blinding_entities": {
            "company_aliases": ["Acme Robotics, Inc.", "Acme Robotics"],
            "founder_names": ["Jane Doe"],
            "portal_names": ["Wefunder"],
            "product_terms": ["AcmeOS"],
        }},
        "t0_payload": {"pitch_text": "Acme Robotics builds AcmeOS with Jane Doe on Wefunder at https://acmerobotics.io.", "financials": {"offering_amount": 50000}},
    }
    b = blind_payload(rec, "blinded_T0")
    txt = b["t0_payload"]["pitch_text"]
    assert "Acme Robotics" not in txt and "Jane Doe" not in txt and "Wefunder" not in txt and "acmerobotics.io" not in txt
    assert "social_cue" not in b["t0_payload"]
    pos = blind_payload(rec, "social_cue_pos")
    neg = blind_payload(rec, "social_cue_neg")
    assert "strong initial commitments" in pos["t0_payload"]["social_cue"]
    assert "slow initial commitments" in neg["t0_payload"]["social_cue"]
    assert len(RUBRIC_DIMENSIONS) == 10
```

- [ ] **Step 3: Run test to verify it fails**
  Run: `.venv\Scripts\python.exe -m pytest tests/test_common.py -v` -> Expected: FAIL (`ModuleNotFoundError: No module named 'src.common'`).

- [ ] **Step 4: Implement `src/common.py`**
  Implement `RUBRIC_DIMENSIONS`, `UNIFIED_SYSTEM_PROMPT_T0` (requesting 10 rubric scores 0–100, `composite_score`, `predicted_invest`, `predicted_invest_prob`, `predicted_survival_prob`, `confidence`, `key_risk_flag`), `SOCIAL_CUE_POS`, `SOCIAL_CUE_NEG`, `build_company_aliases`, and `blind_payload` (case-insensitive boundary masking longest-first, preserving `t0_payload["financials"]` unchanged).

- [ ] **Step 5: Run tests and commit**
  Run: `.venv\Scripts\python.exe -m pytest tests/test_common.py -v` -> Expected: PASS.
  Commit: `git add requirements.txt src/ tests/test_common.py && git commit -m "feat: add shared schema, unified prompt, and entity blinding"`

---

### Task 2: Track 1 SEC EDGAR Form C Crawler & Two-Stage Outcome Coder (`src/ingest/ingest_sec_form_c.py`)

**Files:**
- Create: `c:\Users\meetp\Desktop\BE\Business-Econ-Research\src\ingest\__init__.py`
- Create: `c:\Users\meetp\Desktop\BE\Business-Econ-Research\src\ingest\ingest_sec_form_c.py`
- Test: `c:\Users\meetp\Desktop\BE\Business-Econ-Research\tests\test_ingest_sec.py`

**Interfaces:**
- Consumes: `src.common.build_company_aliases`
- Produces:
  - `parse_cu_amount_raised(xml_text: str) -> float | None`
  - `parse_ctr_is_failure(xml_text: str) -> bool | None` (`True` = cessation/dissolution, `False` = acquisition/threshold exit, `None` = unclear)
  - `code_issuer_outcomes(submissions: list[dict], c_tr_flags: dict[str, bool | None], has_form_d_post: bool, website_alive: bool) -> dict`
  - CLI `ingest_sec_form_c.py --target-n 180` writing `data/processed/track1_sec_form_c.jsonl`, `data/processed/sec_population_counts.json`, and `data/processed/track1_audit_sample_20.csv`.

- [ ] **Step 1: Write failing tests in `tests/test_ingest_sec.py`**
```python
from src.ingest.ingest_sec_form_c import parse_cu_amount_raised, parse_ctr_is_failure, code_issuer_outcomes

def test_parse_cu_and_ctr_xml_variants():
    assert parse_cu_amount_raised("<progressUpdate><amountRaised>125000.50</amountRaised></progressUpdate>") == 125000.50
    assert parse_cu_amount_raised("<other/>") is None
    assert parse_ctr_is_failure("<termination><reason>Ceased operations and dissolved</reason></termination>") is True
    assert parse_ctr_is_failure("<termination><over25MillionAssets>true</over25MillionAssets></termination>") is False

def test_code_issuer_outcomes_two_stage_and_delinquency_fallback():
    funded_alive = code_issuer_outcomes(
        submissions=[{"type": "C", "date": "20190301"}, {"type": "C-AR", "date": "20230401"}],
        c_tr_flags={}, has_form_d_post=False, website_alive=False,
    )
    assert funded_alive["funded_outcome"] == 1 and funded_alive["survival_3y_outcome"] == 1

    delinquent_rescued = code_issuer_outcomes(
        submissions=[{"type": "C", "date": "20190301"}, {"type": "C-AR", "date": "20200401"}],
        c_tr_flags={}, has_form_d_post=True, website_alive=False,
    )
    assert delinquent_rescued["survival_3y_outcome"] == 1 and delinquent_rescued["winner_breakout_outcome"] == 1

    unfunded = code_issuer_outcomes(
        submissions=[{"type": "C", "date": "20190301"}, {"type": "C-W", "date": "20190601"}],
        c_tr_flags={}, has_form_d_post=False, website_alive=True,
    )
    assert unfunded["funded_outcome"] == 0 and unfunded["survival_3y_outcome"] is None
```

- [ ] **Step 2: Run test to verify it fails**
  Run: `.venv\Scripts\python.exe -m pytest tests/test_ingest_sec.py -v` -> Expected: FAIL.

- [ ] **Step 3: Implement `src/ingest/ingest_sec_form_c.py`**
  Download/cache SEC quarterly ZIPs (`2018q1_cf.zip`–`2026q3_cf.zip`) into `data/raw/sec/`, deduplicate to earliest `Form C` per `CIK` in 2018Q1–2020Q4, record full population cell counts (`sec_population_counts.json`), query EDGAR `submissions/CIK{cik}.json` for `C-U` `amount_raised`, `C-TR` `primary_doc.xml`, and post-$T_0$ `Form D` filings, check `ISSUERWEBSITE` liveness for `C-AR`-delinquent funded issuers, sample stratified $N = 150$–$200$ across (`unfunded`, `funded_failed`, `funded_survived`) with `offeringmemoformc.pdf` text $\ge 400$ words (truncated to 18,000 chars) + $T_0$ financials, and export a 20-row random audit CSV (`track1_audit_sample_20.csv`).

- [ ] **Step 4: Run unit tests, then execute live SEC crawl**
  Run: `.venv\Scripts\python.exe -m pytest tests/test_ingest_sec.py -v` -> Expected: PASS.
  Run live ingestion (outside sandbox) and verify `track1_sec_form_c.jsonl` has $150$–$200$ records, zero empty memos, and `sec_population_counts.json` populated.

- [ ] **Step 5: Commit**
  Commit: `git add src/ingest/ingest_sec_form_c.py tests/test_ingest_sec.py && git commit -m "feat: add SEC Form C crawler and two-stage outcome coder"`

---

### Task 3: Track 2 YC Tier-A Harvester (`src/ingest/ingest_yc_tier_a.py`)

**Files:**
- Create: `c:\Users\meetp\Desktop\BE\Business-Econ-Research\src\ingest\ingest_yc_tier_a.py`
- Test: `c:\Users\meetp\Desktop\BE\Business-Econ-Research\tests\test_ingest_yc.py`

**Interfaces:**
- Consumes: `c:\Users\meetp\Desktop\BE\option_b_tier_a_queue_21_v2.jsonl`, `src.common.build_company_aliases`
- Produces:
  - `extract_clean_text_from_html(html: str) -> str`
  - `build_track2_record(raw_rec: dict, harvested_text: str | None, yc_oss_status: str | None) -> dict | None`
  - CLI writing `data/processed/track2_yc_tier_a.jsonl`

- [ ] **Step 1: Write failing tests in `tests/test_ingest_yc.py`**
```python
from src.ingest.ingest_yc_tier_a import build_track2_record

def test_build_track2_record_skips_unpopulated_and_censors_recent():
    pending = {"record_id": "OPTB-016", "meta": {"t0_text_status": "pending_text_ingestion", "accelerator_decision": 1, "three_year_outcome": 1, "blinding_entities": {"company_aliases": ["Xendit"], "founder_names": [], "product_terms": []}}, "blended_pitch_text": {"batch_cycle": "YC S15", "one_liner_and_product": None}}
    assert build_track2_record(pending, None, "Active") is None

    edicek = {"record_id": "OPTB-052", "meta": {"t0_text_status": "populated_ready", "accelerator_decision": 0, "three_year_outcome": None, "blinding_entities": {"company_aliases": ["Edicek"], "founder_names": ["Petr Homoky"], "product_terms": []}}, "blended_pitch_text": {"batch_cycle": "YC S25", "one_liner_and_product": "Edicek is a bookmarking app."}}
    out = build_track2_record(edicek, None, None)
    assert out is not None and out["outcomes"]["survival_3y_outcome"] is None
```

- [ ] **Step 2: Run test to verify it fails**
  Run: `.venv\Scripts\python.exe -m pytest tests/test_ingest_yc.py -v` -> Expected: FAIL.

- [ ] **Step 3: Implement `src/ingest/ingest_yc_tier_a.py`**
  Reuse the 4 `populated_ready` records, fetch live blogs (`about.gitlab.com`, `ethanfast.com`, `nancyhua.com`, `blog.zactownsend.com`, `makersclaw.com`) + Wayback snapshots (`OPTB-004`, `006` PDF, `009`, `010`, `012`, `014`, `017` Staffjoy) + verified extras (`FamilyLeaf`, `80,000 Hours`, `Simple Habit`, `Slite`, `Dendron`), cross-check outcomes against `yc-oss/api`, and exclude any URL whose verbatim $T_0$ text cannot be extracted cleanly.

- [ ] **Step 4: Run unit tests and live Track 2 harvest**
  Run: `.venv\Scripts\python.exe -m pytest tests/test_ingest_yc.py -v` -> Expected: PASS.
  Run live harvest and verify `track2_yc_tier_a.jsonl` contains $\ge 15$ verified records including `OPTB-017` (Staffjoy) and `OPTB-051` (Buffer).

- [ ] **Step 5: Commit**
  Commit: `git add src/ingest/ingest_yc_tier_a.py tests/test_ingest_yc.py && git commit -m "feat: add Track 2 YC Tier-A harvester with Wayback fallback"`

---

### Task 4: $T_0$ Firewall & Blinding Verification Gate (`src/ingest/audit_t0_firewall.py`)

**Files:**
- Create: `c:\Users\meetp\Desktop\BE\Business-Econ-Research\src\ingest\audit_t0_firewall.py`
- Test: `c:\Users\meetp\Desktop\BE\Business-Econ-Research\tests\test_audit_firewall.py`

**Interfaces:**
- Consumes: `src.common.blind_payload`, `data/processed/track1_sec_form_c.jsonl`, `data/processed/track2_yc_tier_a.jsonl`
- Produces:
  - `audit_record(record: dict) -> list[str]` (returns list of violation strings; empty = pass)
  - `run_audit(jsonl_paths: list[str], report_path: str) -> bool`

- [ ] **Step 1: Write failing tests in `tests/test_audit_firewall.py`**
```python
from src.ingest.audit_t0_firewall import audit_record

def test_audit_record_catches_leakage_and_unmasked_alias():
    leaky = {
        "record_id": "TEST-1",
        "track": "track1_sec",
        "meta": {"blinding_entities": {"company_aliases": ["Acme"], "founder_names": [], "portal_names": [], "product_terms": []}},
        "t0_payload": {"pitch_text": "We were acquired by Google in 2022 after raising Series A."},
    }
    issues = audit_record(leaky)
    assert any("leakage" in i.lower() for i in issues)
```

- [ ] **Step 2: Run test to verify it fails**
  Run: `.venv\Scripts\python.exe -m pytest tests/test_audit_firewall.py -v` -> Expected: FAIL.

- [ ] **Step 3: Implement `src/ingest/audit_t0_firewall.py`**
  Check every record for post-$T_0$ leakage patterns (`acquired by`, `shut down`, `bankrupt`, `ceased operations`, `IPO`) and verify `blind_payload(rec, "blinded_T0")` contains zero remaining aliases/founder/portal/URL substrings; write `data/processed/firewall_audit_report.json` and exit non-zero if any record fails.

- [ ] **Step 4: Run tests and audit live Track 1 + Track 2 JSONLs**
  Run: `.venv\Scripts\python.exe -m pytest tests/test_audit_firewall.py -v` -> Expected: PASS.
  Run `.venv\Scripts\python.exe -m src.ingest.audit_t0_firewall` -> Expected: exit 0, 0 violations.

- [ ] **Step 5: Commit**
  Commit: `git add src/ingest/audit_t0_firewall.py tests/test_audit_firewall.py && git commit -m "feat: add T0 leakage and entity-blinding audit gate"`

---

### Task 5: Resumable 4-Condition Gemini Experiment Runner (`src/eval/run_llm_experiment.py`)

**Files:**
- Create: `c:\Users\meetp\Desktop\BE\Business-Econ-Research\src\eval\__init__.py`
- Create: `c:\Users\meetp\Desktop\BE\Business-Econ-Research\src\eval\run_llm_experiment.py`
- Test: `c:\Users\meetp\Desktop\BE\Business-Econ-Research\tests\test_run_llm.py`

**Interfaces:**
- Consumes: `src.common.{UNIFIED_SYSTEM_PROMPT_T0, RUBRIC_DIMENSIONS, blind_payload}`, `data/processed/track1_sec_form_c.jsonl`, `data/processed/track2_yc_tier_a.jsonl`
- Produces:
  - `load_completed_keys(csv_path: str) -> set[tuple[str, str, int]]`
  - `run_experiment(jsonl_paths: list[str], output_csv: str, n_runs: int = 3, temperature: float = 0.2, limit: int | None = None) -> None`
  - Output CSV `results/llm_scores_raw.csv`

- [ ] **Step 1: Write failing tests in `tests/test_run_llm.py`**
```python
from src.eval.run_llm_experiment import run_experiment, load_completed_keys
import json, csv

def test_run_experiment_resumes_and_flushes(tmp_path, monkeypatch):
    jsonl = tmp_path / "data.jsonl"
    rec = {"record_id": "SEC-1", "track": "track1_sec", "meta": {"blinding_entities": {"company_aliases": ["Acme"], "founder_names": [], "portal_names": [], "product_terms": []}}, "t0_payload": {"pitch_text": "Acme builds tools."}}
    jsonl.write_text(json.dumps(rec) + "\n", encoding="utf-8")
    out_csv = tmp_path / "scores.csv"
    calls = []
    def fake_gemini(prompt, **kw):
        calls.append(prompt)
        return {"scores": {d: 70 for d in ["team_and_background","execution_plan","financial_feasibility","writing_and_polish","value_proposition_innovativeness","market_opportunity","competitive_moat","customer_need_alignment","roi_potential","long_run_viability"]}, "composite_score": 70.0, "predicted_invest": 1, "predicted_invest_prob": 0.72, "predicted_survival_prob": 0.65, "confidence": 75, "key_risk_flag": "Early market."}
    monkeypatch.setattr("src.eval.run_llm_experiment.call_gemini_json", fake_gemini)
    run_experiment([str(jsonl)], str(out_csv), n_runs=2)
    assert len(calls) == 8  # 4 arms * 2 runs
    assert len(load_completed_keys(str(out_csv))) == 8
    run_experiment([str(jsonl)], str(out_csv), n_runs=2)
    assert len(calls) == 8  # Resumed without duplicate calls
```

- [ ] **Step 2: Run test to verify it fails**
  Run: `.venv\Scripts\python.exe -m pytest tests/test_run_llm.py -v` -> Expected: FAIL.

- [ ] **Step 3: Implement `src/eval/run_llm_experiment.py`**
  Implement `call_gemini_json` (reading `GEMINI_API_KEY` from `os.environ`, targeting `gemini-2.5-flash`, with 3-attempt exponential backoff on HTTP 429/5xx or malformed JSON), `load_completed_keys`, and `run_experiment` (iterating the 4 arms $\times$ `n_runs`, flushing every row immediately).

- [ ] **Step 4: Run tests, smoke-test `--limit 2`, then run full scoring**
  Run: `.venv\Scripts\python.exe -m pytest tests/test_run_llm.py -v` -> Expected: PASS.
  With user's `GEMINI_API_KEY` in env, run `--limit 2` first to verify schema, then run full `run_llm_experiment.py` across Track 1 + Track 2.

- [ ] **Step 5: Commit**
  Commit: `git add src/eval/run_llm_experiment.py tests/test_run_llm.py && git commit -m "feat: add resumable 4-condition Gemini experiment runner"`

---

### Task 6: Econometric, ML & Error Analysis Pipeline (`src/analysis/analyze_results.py`)

**Files:**
- Create: `c:\Users\meetp\Desktop\BE\Business-Econ-Research\src\analysis\__init__.py`
- Create: `c:\Users\meetp\Desktop\BE\Business-Econ-Research\src\analysis\analyze_results.py`
- Test: `c:\Users\meetp\Desktop\BE\Business-Econ-Research\tests\test_analyze_results.py`

**Interfaces:**
- Consumes: `results/llm_scores_raw.csv`, `data/processed/track1_sec_form_c.jsonl`, `data/processed/track2_yc_tier_a.jsonl`, `data/processed/sec_population_counts.json`
- Produces:
  - `compute_paired_ablation(df_agg: pd.DataFrame, arm_a: str, arm_b: str) -> dict`
  - `compute_oof_ensemble(df: pd.DataFrame, y_col: str, feature_cols: list[str], n_splits: int = 5) -> dict`
  - CLI writing `results/analysis_summary.json` and 4 PNG figures in `results/figures/` (`fig1_blinding_memorization.png`, `fig2_herding_cues.png`, `fig3_roc_pr_curves.png`, `fig4_calibration_and_errors.png`).

- [ ] **Step 1: Write failing tests in `tests/test_analyze_results.py`**
```python
import pandas as pd, numpy as np
from src.analysis.analyze_results import compute_paired_ablation, compute_oof_ensemble

def test_paired_ablation_and_oof_ensemble():
    df = pd.DataFrame({
        "record_id": ["A","B","C","D","A","B","C","D"],
        "evaluation_mode": ["blinded_T0"]*4 + ["unblinded_T0"]*4,
        "composite_score": [50.0, 60.0, 55.0, 65.0, 60.0, 70.0, 65.0, 75.0],
        "predicted_invest": [0, 1, 0, 1, 1, 1, 1, 1],
    })
    res = compute_paired_ablation(df, "unblinded_T0", "blinded_T0")
    assert abs(res["mean_delta"] - 10.0) < 1e-6

    rng = np.random.default_rng(42)
    ens_df = pd.DataFrame({
        "llm_score": rng.normal(60, 10, 40),
        "funding_ratio": rng.uniform(0.5, 2.5, 40),
        "y": ([0, 1] * 20),
    })
    oof = compute_oof_ensemble(ens_df, "y", ["llm_score", "funding_ratio"], n_splits=5)
    assert 0.0 <= oof["roc_auc"] <= 1.0 and len(oof["oof_probs"]) == 40
```

- [ ] **Step 2: Run test to verify it fails**
  Run: `.venv\Scripts\python.exe -m pytest tests/test_analyze_results.py -v` -> Expected: FAIL.

- [ ] **Step 3: Implement `src/analysis/analyze_results.py`**
  Implement reliability (ICC/Cronbach's $\alpha$), paired $t$/Wilcoxon tests ($\Delta_{\text{mem}}$, $\Delta_{\text{herd}}$, decision-flip rate), Stage 1 & Stage 2 nested logits (unweighted + IPW population-weighted), ROC-AUC/PR-AUC/Brier calibration, raw vs. base-rate-matched confusion matrices, out-of-fold CV $H_4$ ensemble (guarding against sparse/single-class folds), and matplotlib figure generation.

- [ ] **Step 4: Run tests and execute full analysis**
  Run: `.venv\Scripts\python.exe -m pytest tests/test_analyze_results.py -v` -> Expected: PASS.
  Run `.venv\Scripts\python.exe -m src.analysis.analyze_results` -> Expected: `results/analysis_summary.json` and 4 PNGs created.

- [ ] **Step 5: Commit**
  Commit: `git add src/analysis/analyze_results.py tests/test_analyze_results.py && git commit -m "feat: add econometric, IPW, OOF ensemble, and figure analysis pipeline"`

---

### Task 7: Publication-Grade BE Research Report (`report/BE_Research_Report.md` & `.docx`)

**Files:**
- Create: `c:\Users\meetp\Desktop\BE\Business-Econ-Research\report\build_docx.py`
- Create: `c:\Users\meetp\Desktop\BE\Business-Econ-Research\report\BE_Research_Report.md`
- Create: `c:\Users\meetp\Desktop\BE\Business-Econ-Research\report\BE_Research_Report.docx`
- Test: `c:\Users\meetp\Desktop\BE\Business-Econ-Research\tests\test_build_docx.py`

**Interfaces:**
- Consumes: `results/analysis_summary.json`, `data/processed/firewall_audit_report.json`, `data/processed/track1_audit_sample_20.csv`, `results/figures/*.png`
- Produces: `render_markdown_to_docx(md_path: str, figures_dir: str, out_docx: str) -> None`

- [ ] **Step 1: Write failing test in `tests/test_build_docx.py`**
```python
from report.build_docx import render_markdown_to_docx
import docx

def test_render_markdown_to_docx_creates_valid_doc(tmp_path):
    md = tmp_path / "sample.md"
    md.write_text("# Title\n\n## 1. INTRODUCTION\n\nBody text with **bold**.\n\n| A | B |\n|---|---|\n| 1 | 2 |\n", encoding="utf-8")
    out = tmp_path / "out.docx"
    render_markdown_to_docx(str(md), str(tmp_path), str(out))
    d = docx.Document(str(out))
    assert any("INTRODUCTION" in p.text for p in d.paragraphs)
    assert len(d.tables) == 1
```

- [ ] **Step 2: Run test to verify it fails**
  Run: `.venv\Scripts\python.exe -m pytest tests/test_build_docx.py -v` -> Expected: FAIL.

- [ ] **Step 3: Implement `report/build_docx.py` and author `report/BE_Research_Report.md`**
  Build `render_markdown_to_docx` supporting headings, styled tables, bullet lists, and embedded PNG figures. Author `BE_Research_Report.md` strictly using verified numbers from `analysis_summary.json` and `firewall_audit_report.json`, structured identically to `Prev year papers/be report.docx` (Objective/Methodology/Findings/Contribution/Limitation/Novelty/Keywords Abstract, Sections 1–6, References, Appendices A–C) with Mermaid conceptual diagrams.

- [ ] **Step 4: Run tests, build `.docx`, and verify zero placeholders**
  Run: `.venv\Scripts\python.exe -m pytest -v` -> Expected: All unit tests PASS.
  Run `.venv\Scripts\python.exe -m report.build_docx` -> Verify `report/BE_Research_Report.docx` opens cleanly and contains 0 `TBD`/`placeholder` tokens.

- [ ] **Step 5: Commit**
  Commit: `git add report/ tests/test_build_docx.py && git commit -m "docs: generate final BE empirical research report and docx builder"`
