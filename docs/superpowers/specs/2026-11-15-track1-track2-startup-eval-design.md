# Design Specification: Dual-Track Empirical Study Extending Csaszar et al. (2024) and Replicating Kleinert & Urbig (2026)

**Date:** 2026-11-15  
**Target Repository:** `c:\Users\meetp\Desktop\BE\Business-Econ-Research` (existing starter files in `c:\Users\meetp\Desktop\BE\`)  
**Course / Discipline:** Business Economics (BE) Research Project  

---

## 1. Intent & Why

This project builds a reproducible empirical study and Business Economics research report modeled on the structure of [be report.docx](file:///c:/Users/meetp/Desktop/BE/Business-Econ-Research/Prev%20year%20papers/be%20report.docx) and conceptually grounded in [csaszar_2024.txt](file:///c:/Users/meetp/Desktop/BE/Business-Econ-Research/Sources/csaszar_2024.txt) and [The_Economics_of_Decision_Authority_in_AI_Strategic_Decision_Making.md](file:///c:/Users/meetp/Desktop/BE/Business-Econ-Research/Prev%20year%20papers/The_Economics_of_Decision_Authority_in_AI_Strategic_Decision_Making.md).

- **Csaszar, Ketkar, & Kim (2024)** (*Strategy Science*) showed that LLM 10-dimension evaluations correlate with human investor scores ($r = 0.52$), but left open whether LLM evaluations predict **realized venture outcomes**.
- **Kleinert & Urbig (2026)** (*Entrepreneurship Theory and Practice*) evaluated 171 archival equity crowdfunding pitches (Crowdcube, 2017–2018) and showed that while LLMs mirror initial fundraising outcomes, apparent survival accuracy can reflect **pre-training memorization of famous digital footprints**, while extra contextual/social cues trigger **anchoring and herding**.
- **Why this design:** Your existing YC files (`option_b_tier_a_queue_21_v2.jsonl`, `option_b_master_register_100_v2.csv`) cannot power an outcome study alone (17 of 21 Tier-A records lack $T_0$ text; Tier-A has only 1 failure; the 50 rejected rows in `option_b_master_register_100_v2.csv` have 0 failures due to `RejectedByYC` survivorship bias). Pairing **Track 1 (U.S. SEC EDGAR Regulation Crowdfunding Form C filings)** with **Track 2 (Audited Verbatim YC Tier-A applications)** creates a clean, $T_0$-firewalled dataset capable of testing both predictive validity ($H_1$–$H_4$) and Kleinert & Urbig's memorization and herding mechanisms.

---

## 2. Goals, Non-Goals, and Anti-Goals

### Goals
1. **Construct Track 1 (Core Empirical Benchmark, $N = 150$–$200$):** Crawl official SEC Regulation Crowdfunding (`Form C`) datasets (2018–2020 baseline offerings) plus EDGAR `offeringmemoformc.pdf` / narrative filings and track longitudinal outcomes through 2026 (`Form C-U`, `C-AR`, `C-TR`, `C-W`) to obtain real **$T_0$ pitch + $T_0$ financials + Fundraising Outcome + 3-to-5+ Year Survival Outcome**.
2. **Construct Track 2 (Famous-Startup Contrast Layer, $N \approx 18$–$22$):** Populate the recoverable pending records in `option_b_tier_a_queue_21_v2.jsonl` via live founder blogs, GitLab/MakersClaw verbatim archives, and Wayback Machine (`archive.org`), cross-checking outcomes against `yc-oss/api`.
3. **Run Controlled LLM Experiments:** Extend `option_b_phase2_pipeline_v2.py` to execute **4 prompt conditions** using `gemini-2.5-flash` ($N = 3$ runs per condition, temperature $T = 0.2$, Csaszar's 10-dimension rubric + unified `predicted_invest`, `predicted_invest_prob`, and `predicted_survival_prob`):
   - **Condition 1 (`blinded_T0`):** Entity/founder/portal/URL-masked $T_0$ full-investor payload (pitch + $T_0$ financials).
   - **Condition 2 (`unblinded_T0`):** Unmasked names/URLs to measure **digital-footprint memorization bias** ($\Delta_{\text{mem}} = \text{Unblinded} - \text{Blinded}$) across obscure (Track 1) vs. famous (Track 2) startups.
   - **Conditions 3–4 (`social_cue_pos` vs. `social_cue_neg`):** Controlled social/herding cue injection at $T_0$ to measure **anchoring & herding bias** ($\Delta_{\text{herd}}$).
4. **Statistical & Econometric Evaluation:** Compute inter-run reliability, paired tests for memorization and herding shifts, two-stage nested logistic regressions (Stage 1 fundraising on full cohort; Stage 2 survival and `Form D`/exit breakout winners on funded issuers with `funding_ratio` + $T_0$ financial controls), population-weighted & unweighted ROC-AUC, PR-AUC, Brier calibration, confusion matrices, out-of-fold $H_4$ ensembles, and failure error analysis.
5. **Publication-Style BE Report:** Generate both Markdown and `.docx` reports matching the exact structural blueprint of [be report.docx](file:///c:/Users/meetp/Desktop/BE/Business-Econ-Research/Prev%20year%20papers/be%20report.docx) (structured Abstract, Sections 1–6, References, Appendices A–C) with clean charts and conceptual Mermaid/architecture diagrams.

### Non-Goals
- No private VC deal-flow CRM partnerships (Tier 3 remains explicitly out of scope).
- No use of synthetic startup datasets (e.g., HuggingFace `Yoav-omer/startups` is excluded).
- No pooling of `RejectedByYC` Tier-C directory leads (which have 0% failure rate and dead links) into primary outcome regressions.
- No interactive web frontend or dashboard.

### Anti-Goals (Failure Modes to Prevent)
- **Look-ahead leakage:** Including any post-$T_0$ text (e.g., `"Acquired by..."`, later funding rounds, `C-AR` post-offering updates, or `yc-oss` `long_description` prose) inside the LLM evaluation prompt.
- **Stratum confounding:** Pooling Track 1 (SEC Form C) and Track 2 (YC applications) into one unstratified regression without stratum indicators or separate reporting.
- **Misinterpreting `Form C-TR`:** Coding every `Form C-TR` termination filing as a business failure (companies can file `C-TR` after acquisition, IPO, or asset thresholds; termination reason / `C-AR` continuity must be audited).
- **Overclaiming on $N \approx 20$:** Running underpowered regressions on Track 2 alone; Track 2 is explicitly used for the famous-startup blinding ablation and qualitative case comparison (`Buffer` vs. `Staffjoy`), while Track 1 ($N = 150$–$200$) carries the primary statistical tests.

---

## 3. Constraints

- **Python Environment:** System `C:\msys64\ucrt64\bin\python.exe` lacks `pip` and third-party libraries. Use `C:\Users\meetp\AppData\Local\Programs\Python\Python314\python.exe` with a dedicated virtual environment (`.venv`) installing `pandas`, `numpy`, `scipy`, `statsmodels`, `scikit-learn`, `matplotlib`, `pypdf`, `beautifulsoup4`, and `python-docx`.
- **Network & Credentials:**
  - `GEMINI_API_KEY` must be read strictly from environment variables at runtime (never committed or logged).
  - SEC EDGAR requires a compliant `User-Agent` header (`BEResearchProject <contact>`) and polite throttling ($\le 5$ requests/second, with exponential backoff on 429/5xx).
- **API Call Budget:**
  - With $N \approx 160$–$180$ total startups (e.g., 150 Track 1 + ~20 Track 2) across 4 prompt conditions (`blinded_T0`, `unblinded_T0`, `social_cue_pos`, `social_cue_neg`) $\times 3$ runs = ~2,040 API calls.
  - Runner must checkpoint every row to disk immediately (`flush()`) and support resuming without re-billing completed `(record_id, arm, run_idx)` tuples.
- **Existing Starter Files:** Preserve existing files in `c:\Users\meetp\Desktop\BE\` (`option_b_master_register_100_v2.csv`, `option_b_tier_a_queue_21_v2.jsonl`, `option_b_phase2_pipeline_v2.py`) as clean inputs/references; house all new code, data, outputs, and reports inside `c:\Users\meetp\Desktop\BE\Business-Econ-Research\`.

---

## 4. Approaches Considered & Chosen

1. **Approach 1 — Track 1 (SEC Form C, $N = 150$–$200$) + Track 2 (Audited YC Tier-A, $N \approx 20$) *(Selected)***
   - *Why:* Replicates Kleinert & Urbig's exact empirical setting (equity crowdfunding with $T_0$ pitch + fundraising + 3–5+ yr survival) on open public filings, while preserving the YC Tier-A cohort for famous-entity memorization contrast.
2. **Approach 2 — Track 2 (YC Tier-A) + `yc-oss` 200-Company Survival Sample *(Rejected)***
   - *Trade-off:* Easy JSON download (3,403 mature companies, 800 `Inactive`), *but* `yc-oss` `long_description`s contain post-YC edits (`"Acquired by Knotel in 2018"`) and `team_size` reflects latest headcount, violating the $T_0$ firewall.
3. **Approach 3 — Full 100-Row Option B CSV Only *(Rejected)***
   - *Trade-off:* Matches original register size, *but* 67 Tier-C rows lack $T_0$ Q&A text (`rejectedbyyc-ten.vercel.app` is 404) and 43/43 non-censored rejected rows succeeded (0 failures), fatally skewing classification.
4. **Approach 4 — Track 1 (SEC Form C) Only *(Rejected)***
   - *Trade-off:* Cleanest single-stratum sample, *but* lacks famous startups where `unblinded_T0` triggers strong pre-training recall, weakening the direct comparison against Csaszar/YC materials already prepared.

---

## 5. System Architecture & Experimental Design

```text
c:\Users\meetp\Desktop\BE\Business-Econ-Research\
├── data/
│   ├── raw/                     # Downloaded SEC ZIPs, Form C PDFs/XMLs, cached YC HTML/Wayback
│   ├── processed/
│   │   ├── track1_sec_form_c.jsonl
│   │   ├── track2_yc_tier_a.jsonl
│   │   └── firewall_audit_report.json
├── src/
│   ├── ingest/
│   │   ├── ingest_sec_form_c.py # SEC quarterly TSV + EDGAR Form C memo crawler & outcome coder
│   │   ├── ingest_yc_tier_a.py  # Live + Wayback + GitLab/MakersClaw harvester for Tier-A
│   │   └── audit_t0_firewall.py # Leakage & entity-blinding verifier
│   ├── eval/
│   │   └── run_llm_experiment.py # Resumable Gemini 2.5 Flash 4-arm runner (N=3, T=0.2)
│   └── analysis/
│       └── analyze_results.py   # Econometrics, AUC/calibration, blinding/herding tests, charts
├── results/
│   ├── llm_scores_raw.csv
│   ├── analysis_summary.json
│   └── figures/                 # PNG charts for report
└── report/
    ├── BE_Research_Report.md
    ├── BE_Research_Report.docx
    └── build_docx.py            # Styled academic Word generator matching be report.docx
```

### 5.1 Track 1 Data Pipeline (`ingest_sec_form_c.py`)
1. **Cohort Window & Deduplication *(our call)*:** Pull SEC `crowdfunding-offerings-data-sets` quarterly ZIPs for **2018Q1–2020Q4** to identify baseline `SUBMISSION_TYPE == "C"` offerings (ensuring a full **5–8 year follow-up window** through 2026Q3), and pull **2018Q1–2026Q3** submission tables to trace every issuer's `CIK` and `FILE_NUMBER` longitudinally. Keep at most **one earliest baseline `Form C` per `CIK`** to prevent duplicate issuer weighting, and persist the **full 2018–2020 population cell counts** *(our call)* for inverse-probability weighting.
2. **Two-Stage Outcome Coding Rules (Eliminates Deterministic Separation):**
   - **Stage 1 — Fundraising Outcome (`funded_outcome`, 1 vs. 0, Full Cohort $N = 150$–$200$):**
     - `1` (Funded): At least one `C-U` progress update confirming target offering amount met/exceeded, OR at least one subsequent `C-AR` annual report filed (under SEC Reg CF, only issuers who close an offering must file `C-AR`). Parse continuous **Human Crowd intensity** (`funding_ratio = amount_raised / offering_amount`) from `Form C-U` `primary_doc.xml` (since `FORM_C_DISCLOSURE.tsv` does not include `amount_raised` directly).
     - `0` (Unfunded / Failed to Close): Explicit `C-W` offering withdrawal, OR offering deadline expired with zero `C-AR` filings and no closing `C-U`.
   - **Stage 2 — 3+ Year Survival & Breakout Winner Outcomes (Funded Cohort $N \approx 100$–$140$):**
     - **`survival_3y_outcome` (`1` vs. `0`):** Coded `1` if the issuer filed `C-AR` annual reports covering fiscal years $\ge 3$ years post-offering, OR filed `C-TR` whose `primary_doc.xml` cites acquisition/growth/asset thresholds, **OR** (for `C-AR`-delinquent issuers) automated verification confirms subsequent EDGAR `Form D` activity or an active issuer website (`HTTP 200` non-parked domain). Coded `0` only if `C-AR` filings ceased within 3 years (or `C-TR` `primary_doc.xml` cites dissolution/cessation) *and* automated `Form D` + website checks confirm inactivity. Supplement with a 20-record manual audit to document label noise.
     - **`winner_breakout_outcome` (`1` vs. `0`, for $H_3$):** Coded `1` if the funded issuer raised subsequent institutional/angel follow-on capital via EDGAR **`Form D`** after $T_0$ or exited via verified acquisition (`C-TR` / directory verification).
3. **Stratified Target Sampling ($N = 150$–$200$):**
   - Sample across 2018–2020 cohorts across three cells (~50 unfunded, ~50–75 funded-failed, ~50–75 funded-survived), restricted to issuers with extractable `offeringmemoformc.pdf` or readable Form C narrative text ($\ge 400$ words) and non-null `OFFERINGAMOUNT` + baseline financials.
4. **Standardized $T_0$ Full-Investor Packet:**
   - Extract pre-close offering memo text (business description, use of proceeds, risk factors/team/market summary, capped cleanly to avoid context bloat) **AND include** structured $T_0$ financials (`offering_amount`, `max_offering`, `security_type`, `employees`, `assets`, `cash`, `debt`, `prior_revenue`, `prior_net_income`) directly in the evaluator payload—mirroring the real information packet available to investors at $T_0$.
   - Store `blinding_entities`: issuer legal/DBA names (including stripped variants without `, Inc.` / `LLC` / `Corp.` suffixes so prose mentions are caught), signatory/officer names from `FORM_C_SIGNATURE.tsv`, portal name (`COMPANYNAME`), and `ISSUERWEBSITE`.

### 5.2 Track 2 Data Pipeline (`ingest_yc_tier_a.py`)
1. Start from the 21 records in `option_b_tier_a_queue_21_v2.jsonl` (4 already `populated_ready`: `OPTB-001` Dropbox, `OPTB-019` PostHog, `OPTB-051` Buffer, `OPTB-052` Edicek).
2. Harvest verbatim $T_0$ Q&As from:
   - **Live URLs:** `OPTB-002` GitLab (`about.gitlab.com/2016/09/30/gitlabs-application-for-y-combinator-winter-2015/`), `OPTB-007` Taazr, `OPTB-011` Apptimize, `OPTB-013` Standard Treasury, `OPTB-015` Mimir (`makersclaw.com/blog/mimir-yc-application-s15`), `OPTB-018` Flex.
   - **Wayback Machine snapshots:** `OPTB-004` Reddit, `OPTB-006` MGWU (`YC+GM.pdf`), `OPTB-009` The Muse, `OPTB-010` Lollipuff, `OPTB-012` One Month, `OPTB-014` Kash, `OPTB-017` Staffjoy (the crucial Tier-A failure).
   - **Additional verified verbatim apps discovered (`rohitdotmittal` / `MakersClaw`):** FamilyLeaf (W12), 80,000 Hours (S15), Simple Habit (W17), Slite (W18), Dendron (W21) as `OPTB-EXT-*` Tier-A additions if full $T_0$ Q&A text parses cleanly.
3. Cross-validate all 3-year outcomes against `yc-oss/api` (`companies/all.json`) and mark any unrecoverable records (`OPTB-003`, `005`, `008`, `016` if still unobtainable) as excluded rather than inventing text. Keep `OPTB-052` (Edicek, YC S25, `<3 yrs`) in the Blinding/Herding ablation while excluding it from 3-year survival tests *(our call)*.

### 5.3 Controlled 4-Condition Unified LLM Experiment (`run_llm_experiment.py`)
All records pass `audit_t0_firewall.py` before scoring. Track 1 and Track 2 use **one unified investor-screening system prompt and output schema** (`predicted_invest` 0/1, `predicted_invest_prob` 0–1, `predicted_survival_prob` 0–1, `confidence` 0–100, Csaszar's 10 rubric dimensions 0–100, `composite_score`, `key_risk_flag`) so cross-track blinding and herding deltas compare directly without prompt-wording confounds. Run `gemini-2.5-flash` ($N = 3$ runs, $T = 0.2$):
1. **`blinded_T0`:** Masked entities/URLs/portals; evaluates pure fundamental $T_0$ text + $T_0$ financials (where present).
2. **`unblinded_T0`:** Same prompt with real startup/founder/portal names intact $\rightarrow$ tests Kleinert & Urbig's **digital-footprint memorization**.
3. **`social_cue_pos` (Herding Positive):** Blinded $T_0$ payload + single controlled cue: *"Note on early campaign reception: Independent early angel diligence was positive, with strong initial commitments ahead of the main close."*
4. **`social_cue_neg` (Herding Negative):** Blinded $T_0$ payload + cue: *"Note on early campaign reception: Early institutional/angel reviewers expressed skepticism, with slow initial commitments ahead of the main close."*

### 5.4 Econometric & Statistical Analysis (`analyze_results.py`)
- **Reliability:** Intraclass correlation / Cronbach's $\alpha$ and score SD across the $N = 3$ runs per arm.
- **Hypothesis & Mechanism Tests:**
  - *Memorization Test (Kleinert & Urbig):* Paired $t$-test & Wilcoxon signed-rank test on $\Delta_{\text{mem}} = \text{Score}_{\text{unblinded}} - \text{Score}_{\text{blinded}}$ and survival AUC delta, comparing Track 1 (obscure Form C) vs. Track 2 (famous YC).
  - *Herding / Anchoring Test (Kleinert & Urbig):* Paired test on $\Delta_{\text{herd}} = \text{Score}_{\text{cue\_pos}} - \text{Score}_{\text{cue\_neg}}$ and decision-flip rate (% of startups flipped from Reject to Invest by the social cue alone).
  - *Stage 1 — Fundraising Prediction ($H_1$, Full Track 1 $N = 150$–$200$):* Logistic regressions predicting `funded_outcome` from `composite_score` (`blinded_T0`) + $T_0$ financial controls; ROC-AUC, PR-AUC, Brier calibration.
  - *Stage 2 — Survival & Winner Prediction ($H_1$–$H_4$, Funded Track 1 $N \approx 100$–$140$):*
    - Nested logistic regressions predicting `survival_3y_outcome` and `winner_breakout_outcome` (`Form D` / exit, $H_3$) from `composite_score` (`blinded_T0`), continuous **Human Crowd funding intensity** (`funding_ratio`), and $T_0$ financial controls.
    - **Population Weighting *(our call)*:** Report *both* unweighted sample estimates and inverse-probability-weighted (population-calibrated) logits, Brier scores, and PR-AUC using the persisted 2018–2020 SEC Reg CF population cell counts.
    - **Cutoffs & $H_4$ Ensemble *(our call)*:** For $2 \times 2$ confusion matrices and F1, report *both* raw LLM binary predictions (`predicted_invest` / 0.50) and base-rate-matched percentile cutoffs; test $H_4$ via out-of-fold cross-validated stacked logit (`Human + LLM`) alongside simple agreement rules (`Both Invest`).
    - Failure-detection lift ($H_2$) vs. breakout-winner recall ($H_3$) and qualitative risk-flag audit.

### 5.5 BE Research Report (`BE_Research_Report.md` & `.docx`)
Follows the exact academic report blueprint of [be report.docx](file:///c:/Users/meetp/Desktop/BE/Business-Econ-Research/Prev%20year%20papers/be%20report.docx) (Objective/Methodology/Findings/Contribution/Limitation/Novelty/Keywords Abstract $\rightarrow$ Sections 1–6 $\rightarrow$ References $\rightarrow$ Appendices A–C with Python details, detailed data tables, and methodology timeline), plus architecture/experimental flow diagrams inspired by [The_Economics_of_Decision_Authority_in_AI_Strategic_Decision_Making.md](file:///c:/Users/meetp/Desktop/BE/Business-Econ-Research/Prev%20year%20papers/The_Economics_of_Decision_Authority_in_AI_Strategic_Decision_Making.md).

---

## 6. Left to the Builder
- Exact PDF extraction library choice (`pypdf` vs. `pdfplumber`) and page/character truncation rules if long Form C memos exceed ~8,000 tokens.
- Exact retry/backoff parameters for SEC EDGAR and Gemini REST API rate limits.
- Visual styling details (matplotlib color palette, figure DPI, Word `.docx` table/heading styles).
