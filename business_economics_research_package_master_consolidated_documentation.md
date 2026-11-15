# Business Economics Research Package: AI vs. Investor Startup Evaluation

**Working Title:** *Can AI Pick Winners? Comparing Large Language Models and Venture Capital Decision-Making Using Historical Startup Outcomes*  
**Discipline:** Business Economics (BE) / Strategic Management  
**Core Literature Anchors:**
- **Problem Statement:** Csaszar, Ketkar, & Kim (2024), *Artificial Intelligence and Strategic Decision-Making: Evidence from Entrepreneurs and Investors*, **Strategy Science**, 9(4):322–345
- **Methodological Diagnosis & Contamination Blueprint:** Kleinert & Urbig, *Startup Evaluations with Generative Artificial Intelligence: An Exploratory Study on Early-Stage Investments and Survival Predictions by Large Language Models*

---

## 1. Executive Summary & Theoretical Architecture

### 1.1 The Conceptual Advance (Csaszar et al., 2024 $\rightarrow$ Kleinert & Urbig $\rightarrow$ Our Study)
1. **The Problem Statement (Csaszar et al., 2024):** Across 138 startup plans and 541 professional VC/angel reviews, GPT-4 correlated with human investor evaluations at $r = 0.52$. However, evaluation similarity does not prove predictive validity or superior capital allocation—an LLM can mirror human VCs while inheriting their cognitive biases and herding behavior.
2. **The Methodological Diagnosis (Kleinert & Urbig):** Evaluating 171 archival pitches under varied information cues, Kleinert & Urbig demonstrate that while LLMs mirror initial fundraising outcomes, their apparent accuracy in predicting long-term venture survival largely reflects **prior pre-training exposure to startups' digital footprints** rather than genuine reasoning under uncertainty, while social cues activate **anchoring and herding**.
3. **Our Project's Contribution & Scope Discipline:** Before running predictive horse-races, we enforce strict provenance auditing, temporal firewalls ($T_0$), entity blinding, and stratum separation across three coordinated artifacts:
   - **Artifact 1 — Audited Pilot Dataset (`v3.1`, $N = 17$):** Source-audited exploratory package (`Business_Econ_v3_1_startup_master.csv`, SHA256 `301af4b9...d0abd30704d1f0f8a6`) with 156 verified business-fact fields across 159 evidence rows, 17 human-decision records, 29 typed event records, and 170 verification-map rows. **No LLM scoring or $H_1$–$H_4$ predictive test has been executed on v3.1.**
   - **Artifact 2 — Unaudited Candidate Lead Register ($N = 52$):** Discovery register (`appendix_startup_leads_52_v4_2.csv`) spanning independent seed decks, Bessemer investment memos, accelerator applications, and crypto-adjacent leads (kept strictly unmerged from v3.1).
   - **Artifact 3 — Option B Standardized YC Application Benchmark ($N = 100$):** Single-format expansion (`option_b_master_register_100_v2.csv`) balanced 50 Accepted vs. 50 Rejected YC applications, paired with a pre-scoring gate and entity-blinding pipeline (`option_b_phase2_pipeline_v2.py`).

### 1.2 Research Questions & Hypotheses (Formal Specification)
- **Primary RQ:** Do LLM investment evaluations predict subsequent startup outcomes more accurately than historical investor decisions when restricted strictly to information available at decision time ($T_0$)?
- **$H_1$ (Predictive Parity):** LLM-generated evaluations predict subsequent startup survival and follow-on funding at least as accurately as historical human decisions.
- **$H_2$ (Asymmetric Failure Detection — "The Lemon Filter"):** LLMs outperform human VCs in identifying early-stage startups that ultimately fail by evaluating unit economics and operational consistency without founder halo effects or FOMO.
- **$H_3$ (Outlier Winner Detection — "The Tacit Knowledge Advantage"):** Human investors outperform LLMs in identifying extreme power-law outliers ("unicorns") that depend on tacit founder grit and private channel checks absent from written text.
- **$H_4$ (Super-Additive Ensembling):** Combining LLM scoring with human investor judgment yields higher predictive accuracy and capital allocation efficiency than either alone.

---

## 2. Literature Synthesis Matrix (Section II Anchor)

| Study Citation | Empirical Setting & Data | Core Methodological Approach | Key Empirical Findings | Role in Our Study |
| :--- | :--- | :--- | :--- | :--- |
| **Csaszar, Ketkar, & Kim (2024)**, *Strategy Science* | 138 startup plans; 541 VC reviews; 250 angel evaluators | RCT + 10-Dimension Rubric Scoring (0–100) | $r = 0.52$ correlation between LLM and VC scores; $+0.14\text{ SD}$ generation boost | **Problem Anchor:** Establishes judgment similarity; leaves realized survival untested |
| **Kleinert & Urbig**, *Startup Evaluations with Generative AI* | 171 archival venture pitches; human investor benchmark | Pre-registered LLM experiments with varied information cues | Mirrors fundraising outcomes; survival accuracy driven by digital-footprint memorization; cues trigger herding | **Methodological Blueprint:** Justifies entity blinding, temporal firewalls, and contamination flags |
| **Gompers, Gornall, Kaplan, & Strebulaev (2020)**, *JFE* | 885 institutional VCs across 681 firms | Institutional survey and deal-flow audit | VCs rank management team ("jockey") #1 and rely heavily on qualitative gut feel | **Human Benchmark:** Explains human vulnerability to founder charisma and halo bias |
| **Kahneman, Sibony, & Sunstein (2021)**, *Noise* | Cross-industry expert decision audits | Variance decomposition (bias vs. noise) | Human committees suffer from severe occasion and sequence noise | **Algorithmic Consistency:** Justifies LLM rubric scoring as a low-noise baseline |
| **Kim, Glaeser, Hillis, Kominers, & Luca (2024)**, *SMJ* | 55 enterprise departments; multi-year field audit | Econometric policy evaluation & override audits | $40\%+$ human override rate; overrides systematically degrade accuracy due to career-risk aversion | **Agency Framework:** Explains committee non-approvals vs. analyst memos (cf. LinkedIn S17) |
| **Guzman & Stern (2015, 2017)**, *Science / AER* | State corporate registries and startup cohorts | Discrete choice modeling from founding observables | $T_0$ observable attributes reliably forecast growth and IPO outcomes | **Methodological Precedent:** Validates that $T_0$ text contains genuine predictive signal |
| **Mollick (2014)**, *Journal of Business Venturing* | 48,500+ crowdfunding campaigns | Econometric regression on pitch linguistics | Pitch text clarity, team size, and goals systematically predict fulfillment/survival | **Textual Signaling:** Supports structured $T_0$ pitch text analysis |
| **Wang et al. (2025)**, *SSFF Preprint* | Early-stage startup pitches & founder profiles | Zero-shot and few-shot LLM classification | High founder-idea fit detection, but strong LLM over-prediction bias on prestige markers | **Prompt Calibration:** Guides temperature scaling ($T = 0.2$) and anti-optimism instructions |
| **Liu et al. (2025)**, *SimVC Preprint* | Multi-agent role-playing VC simulation | LLM agent committee debate and voting | Multi-agent debate outperforms single-agent LLM predictions | **Ensembling Design:** Supports structured multi-dimension rubric aggregation |

---

## 3. Audited Pilot Dataset (`v3.1`, $N = 17$) — Architecture & Safeguards

### 3.1 Analytical Stratification & Audit Restrictions
Across the 17 records in `Business_Econ_v3_1_startup_master.csv`, 3-year follow-on financing labels (`follow_on_financing_3y`) contain **12 positives (`1`)**, **1 inherited terminal-history negative (`0`, Everpix)**, and **4 unknown/censored labels (`NaN`)**. Human decision signals (`human_signal`) record **14 affirmative signals (`1`)**, **2 non-admissions/non-approvals (`0`: Buffer YC rejection and LinkedIn March 2008 committee non-approval)**, and **1 unassigned (`NaN`, Everpix)**.

| v3.1 Benchmark Stratum | $N$ | Companies (ID) | Artifact & Decision Structure | Audit Qualification & Analytical Restriction |
| :--- | :---: | :--- | :--- | :--- |
| `primary_vc_observable_proxy` | 3 | Okteto (S06), Esper (S09), Meroxa (S11) | Edited investor memos (2018–2020); all 3 affirmative VC seed investments; all 3 financing-positive at 3y | Only true seed-period VC proxies in v3.1, but 100% funded (zero rejections). Cannot support rejection-accuracy tests. |
| `secondary_accelerator` | 4 | Buffer (S01), Dropbox (S02), GitLab (S03), Mixpanel (S04) | YC written applications (2007–2015); 3 accepted (S02–S04), 1 rejected (S01 Buffer, W11 batch applied late 2010); all 4 financing-positive | Accelerator admission/rejection is not equivalent to institutional VC investment/pass; high recall contamination risk. |
| `secondary_recommendation` | 2 | YouTube (S05), Zed (S12) | Partial scanned 2005 memo (YouTube) & 2021 edited memo (Zed); both affirmative signals & financing-positive | Analyst/partner recommendation memo is not verified committee execution or complete private diligence packet. |
| `separate_declined_lead` | 1 | Everpix (S13) | Company-published Aug 2013 pitch deck; `follow_on_financing_3y = 0` (shut down); `human_signal = NaN` | Inherited terminal-history failure; lacks a matched, dated individual VC rejection artifact. |
| `vc_undated_descriptive` | 2 | Privacy Dynamics (S07), Superconductive / Great Expectations (S10) | Edited investor memos; seed close dates unverified; follow-on financing = `NaN` | Descriptive inputs only; excluded from fixed-horizon 3-year outcome benchmarks. |
| `vc_episode_sensitivity` | 1 | Daily (S08) | Edited investor memo (2019/2020); affirmative VC signal & financing-positive | Retained strictly for episode-level sensitivity checks due to broad candidate date window. |
| Post-round / post-decision / timing sensitivity | 3 | Front (S14), Shyp (S15), Homejoy (S16) | S14 deck published Aug 2016 after May Series A; S15 Sep 2013 public solicitation after VC commits; S16 bundled A/B dates unknown | Excluded from verified pre-decision comparisons; retained solely to test sensitivity to post-round revision and timing ambiguity. |
| `vc_later_stage_committee_nonapproval_reproduction_sensitivity` | 1 | LinkedIn (S17) | Investor-linked March 2008 39-page Series D memo reproduction (published Oct 2015); `human_signal = 0`; follow-on = `NaN` | Later-stage institutional non-approval sensitivity only. Author recommendation and committee non-approval are distinct; same-Series-D extension is not distinct follow-on financing. |

### 3.2 Key Audit Safeguards
1. **Strict Separation of Evaluator Inputs from Ground-Truth Labels:** Only source-based fact paraphrases in `inputs/S01.json`–`inputs/S17.json` (and `inputs/t0_inputs.jsonl`) are candidate evaluator inputs. All decision labels, 3-year outcomes, verification maps, and audit notes remain strictly outside the model prompt. `strict_identical_information` is coded `not_established` across all 17 rows.
2. **Resolution of LinkedIn Memo Provenance (`v3.1 S17` vs. `Appendix REC-034`):** `S17` in v3.1 uses Bessemer Venture Partners' March 2008 39-page Series D memo reproduction (published Oct 2015, committee non-approval sensitivity). Separately, BVP's public archive (`bvp.com/memos/linkedin`) hosts Jeremy Levine's **December 11, 2006** Series C investment memo recommending investment (closed Jan 2007), which is accurately recorded as `REC-034` in the leads appendix.
3. **Live Dataset Admissions Boundary:** Live November 14 lead checks admitted zero Airbnb or Solana records into v3.1.

### 3.3 Complete v3.1 Master Table Inventory ($N = 17$)

| ID | Company | Source Artifact & Period | Benchmark Stratum | 3y Fin / Signal | Matched VC & Eligibility Qualification |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **S01** | Buffer | YC application (W11 batch, applied late 2010) | `secondary_accelerator` | Fin: `1` / Sig: `0` | `no_or_not_this_decision` \| `see_existing_case_specific_provenance_no_upgrade` |
| **S02** | Dropbox | YC application (2007) | `secondary_accelerator` | Fin: `1` / Sig: `1` | `no_or_not_this_decision` \| `see_existing_case_specific_provenance_no_upgrade` |
| **S03** | GitLab | YC application (2014/2015) | `secondary_accelerator` | Fin: `1` / Sig: `1` | `no_or_not_this_decision` \| `see_existing_case_specific_provenance_no_upgrade` |
| **S04** | Mixpanel | YC application (2009) | `secondary_accelerator` | Fin: `1` / Sig: `1` | `no_or_not_this_decision` \| `see_existing_case_specific_provenance_no_upgrade` |
| **S05** | YouTube | partial scanned VC memo (2005-09-02) | `secondary_recommendation` | Fin: `1` / Sig: `1` | `no_or_not_this_decision` \| `see_existing_case_specific_provenance_no_upgrade` |
| **S06** | Okteto | edited investor memo (2020) | `primary_vc_observable_proxy` | Fin: `1` / Sig: `1` | `yes` \| `see_existing_case_specific_provenance_no_upgrade` |
| **S07** | Privacy Dynamics | edited investor memo | `vc_undated_descriptive` | Fin: `NaN` / Sig: `1` | `yes` \| `see_existing_case_specific_provenance_no_upgrade` |
| **S08** | Daily | edited investor memo (2019/2020) | `vc_episode_sensitivity` | Fin: `1` / Sig: `1` | `yes` \| `see_existing_case_specific_provenance_no_upgrade` |
| **S09** | Esper | edited investor memo (2018-02) | `primary_vc_observable_proxy` | Fin: `1` / Sig: `1` | `yes` \| `see_existing_case_specific_provenance_no_upgrade` |
| **S10** | Superconductive / Great Expectations | edited investor memo (2019; memo narrative only; seed close unknown) | `vc_undated_descriptive` | Fin: `NaN` / Sig: `1` | `yes` \| `see_existing_case_specific_provenance_no_upgrade` |
| **S11** | Meroxa | edited investor memo (2020-07-17) | `primary_vc_observable_proxy` | Fin: `1` / Sig: `1` | `yes` \| `see_existing_case_specific_provenance_no_upgrade` |
| **S12** | Zed | edited investor memo (2021) | `secondary_recommendation` | Fin: `1` / Sig: `1` | `no_or_not_this_decision` \| `see_existing_case_specific_provenance_no_upgrade` |
| **S13** | Everpix | company-published pitch deck (2013-08) | `separate_declined_lead` | Fin: `0` / Sig: `NaN` | `no_or_not_this_decision` \| `see_existing_case_specific_provenance_no_upgrade` |
| **S14** | Front | Series A founder-published deck, original version not established (Apr–May 2016 proxy) | `vc_post_round_published_deck_sensitivity` | Fin: `1` / Sig: `1` | `episode_proxy_only` \| `not_established_post_round_published_version` |
| **S15** | Shyp | Investor public solicitation, not complete private VC packet (Sep 23, 2013 proxy) | `vc_post_decision_marketing_sensitivity` | Fin: `1` / Sig: `1` | `episode_proxy_only` \| `not_eligible_for_named_VCs_already_committed` |
| **S16** | Homejoy | Contemporary August operating profile; bundled later-round proxy (Aug–Dec 2013) | `vc_public_info_timing_unverified_sensitivity` | Fin: `NaN` / Sig: `1` | `episode_proxy_only` \| `not_established_actual_decision_dates_unknown` |
| **S17** | LinkedIn | Investor-linked March 2008 Series D recommendation reproduction, 39 pages | `vc_later_stage_committee_nonapproval_reproduction_sensitivity` | Fin: `NaN` / Sig: `0` | `documented_institutional_nonapproval_not_executed_investment` \| `not_established_original_committee_packet_version_unverified` |

---

## 4. Three-Tier Empirical Feasibility & Econometric Specification

### 4.1 Three-Tier Feasibility Matrix
- **Tier 1 — Funded-Only Follow-On Financing / Survival Benchmark (Feasible):** Tests whether ex-ante LLM scoring predicts 3-year follow-on financing or survival *conditional on receiving initial funding* (contrasting funded survivors against funded shutdowns).
- **Tier 2 — Accelerator Admission / Rejection Text Benchmark (Feasible with Caveats):** Benchmarks LLM rubric scores against Y Combinator batch decisions on standardized written application Q&As, provided entity recall is controlled via name-masking and results are not generalized to institutional VC investing.
- **Tier 3 — Head-to-Head "AI vs. VC" Investment & Pass Accuracy Test (Not Feasible on Public Data):** VCs do not publish rejected pitch decks alongside contemporaneous pass memos. Executing Tier 3 requires a private data-sharing partnership with an institutional VC firm's deal-flow CRM.

### 4.2 Econometric Horse-Race & Simulated Allocation Framework
For eligible, blinded $T_0$ records, nested and non-nested binary logit models evaluate incremental predictive power:
$$\text{logit}\left(\mathbb{P}(\text{Outcome}_i = 1)\right) = \beta_0 + \beta_1 \text{Score}_{i, \text{LLM}} + \beta_2 \text{Decision}_{i, \text{Human}} + \mathbf{\Gamma}' \mathbf{X}_i + \varepsilon_i$$
- **Rubric Dimensions (Csaszar et al., 2024):** (1) Team & Background, (2) Execution Plan, (3) Financial Feasibility, (4) Writing & Polish, (5) Value Proposition Innovativeness, (6) Market Opportunity, (7) Competitive Moat, (8) Customer Need Alignment, (9) ROI Potential, (10) Long-Run Viability — scored 0–100 across $N = 3$ runs at temperature $T = 0.2$ under both **Blinded (`blinded_T0`)** and **Unblinded (`unblinded_T0`)** conditions.

---

## 5. Unaudited Candidate Lead Register ($N = 52$ — Synchronized `v4_2`)

**Provenance Disclosure:** These 52 records are candidate leads, not audited v3.1 inputs. Of the **8** rows labeled `rejected` (3 Main List + 5 Flagged Accelerator), only **3** possess contemporaneous dated rejection artifacts (`REC-001` Airbnb June–July 2008 deck + pass emails; `REC-004` Buffer W11 batch application + rejection email; `REC-005` Edicek Spring 2025 YC application + rejection). The remaining **5** (`REC-002`, `REC-003`, `REC-006`, `REC-007`, `REC-008`) rely on retrospective accounts. In the Main List, `REC-015` (Vungle) and `REC-017` (Dwolla) are classified under *Funded - Success/Alive* (8 failed / 24 success/alive), and `REC-044` (Per Diem) is flagged for weak third-party provenance.

| ID | Stratum | Startup & Stage | Date | Decision & Artifact Provenance | ~3 Yr Outcome |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **REC-001** | Main List (Rejection) | Airbnb (AirBed & Breakfast) [Pre-seed] | 2008-06-26 to 2008-07-15 | `rejected` — Contemporaneous 14-slide 2008 Pitch Deck + 5 verbatim dated pass emails ([SlideShare](https://www.slideshare.net/slideshow/airbnb-pitch-deck-from-2008/65585661) / [Medium](https://medium.com/@bchesky/7-rejections-7d894cbaa084)) | Raised more / Scaled |
| **REC-002** | Main List (Rejection) | Airbnb - USV Pass [Seed] | 2008-12 to 2009-02 | `rejected` — Retrospective account / post-hoc narrative ([AVC](https://avc.com/2011/03/airbnb/)) | Raised more / Scaled |
| **REC-003** | Main List (Rejection) | Pandora Media (Savage Beast) [Seed] | 2000-03 to 2001-09 | `rejected` — Retrospective account (~300+ VCs; no named dated pass artifact) | Alive -> Raised later |
| **REC-004** | Flagged: Accel. Rejection | Buffer (YC W11 App) [Pre-seed] | W11 batch (applied late 2010) | `rejected` — Verbatim YC W11 Written App + dated rejection PDF ([Buffer Blog](https://buffer.com/resources/buffers-y-combinator-application/)) | Raised more / Alive |
| **REC-005** | Flagged: Accel. Rejection | Edicek (YC S25 App) [Pre-seed / Idea] | 2025-04 to 2025-05 | `rejected` — Verbatim YC S25 Written App ([Petr Homoky Blog](https://homoky.cz/blog/my-yc-rejection-full-application)) | Alive (<3 yrs elapsed) |
| **REC-006** | Flagged: Accel. Rejection | Relate (Attempt #5 - YC W22) [Pre-seed] | 2021-10 to 2021-11 | `rejected` — Retrospective account ([Relate Blog](https://relate.so/blog/six-applications-y-combinator/)) | Raised more (YC S22) |
| **REC-007** | Flagged: Accel. Rejection | Replit (YC Rejections #1–#3) [Pre-seed] | 2016 to 2017 | `rejected` — Retrospective account ([Replit Blog](https://replit.com/blog/yc)) | Raised more / Scaled |
| **REC-008** | Flagged: Accel. Rejection | Reddit / My Mobile Menu (YC S05) [Idea] | 2005-04 | `rejected` — Retrospective account / YC S05 interview notes | Pivoted -> Acquired |
| **REC-009** | Main List (Funded - Failed) | Flowtab [Seed] | 2012 | `funded` ($110K) — 10-slide 2012 Seed Pitch Deck | Dead |
| **REC-010** | Main List (Funded - Failed) | Lance [Seed] | 2021 | `funded` ($2.8M) — 22-slide 2021 Seed Pitch Deck | Dead |
| **REC-011** | Main List (Funded - Failed) | Binpress [Seed] | 2014 | `funded` ($300K–$420K) — 2014 Seed Pitch Deck | Dead |
| **REC-012** | Main List (Funded - Failed) | Zirtual [Seed] | 2013 | `funded` ($2M) — 2013 Seed Pitch Deck | Dead |
| **REC-013** | Main List (Funded - Failed) | Standout Jobs [Seed] | 2008 | `funded` ($1.8M) — 2008 Seed Pitch Deck | Dead |
| **REC-014** | Main List (Funded - Failed) | Apteo [Pre-seed] | 2019 | `funded` ($1M) — 2019 Pre-Seed Pitch Deck | Dead |
| **REC-015** | Main List (Funded - Success/Alive) | Vungle [Seed] | 2012 | `funded` ($2M) — 2012 Seed Pitch Deck | Raised more / Acquired |
| **REC-016** | Main List (Funded - Failed) | Poliana [Seed] | 2013 | `funded` (Seed) — 2013 Seed Pitch Deck | Dead |
| **REC-017** | Main List (Funded - Success/Alive) | Dwolla [Seed] | 2010 | `funded` ($1.3M) — 2010 Seed Pitch Deck | Raised more / Operating |
| **REC-018** | Main List (Funded - Failed) | AppVirality [Seed] | 2015 | `funded` ($465K) — 2015 Seed Pitch Deck | Dead |
| **REC-019** | Main List (Funded - Success/Alive) | Buffer (Late 2011 Seed) [Seed] | 2011-11 | `funded` ($450K) — 13-slide 2011 Seed Pitch Deck | Alive & Profitable |
| **REC-020** | Main List (Funded - Success/Alive) | Intercom [Seed] | 2012-01 | `funded` ($1M) — 2012 Seed Pitch Deck | Raised more / Scaled |
| **REC-021** | Main List (Funded - Success/Alive) | Canva [Seed] | 2012–2013 | `funded` ($3M) — 2012–2013 Seed Pitch Deck | Raised more / Scaled |
| **REC-022** | Main List (Funded - Success/Alive) | Revolut [Seed] | 2015 | `funded` (£1.5M) — 14-slide 2015 Seed Pitch Deck | Raised more / Scaled |
| **REC-023** | Main List (Funded - Success/Alive) | Wealthsimple [Seed] | 2014 | `funded` (CA$2M) — 2014 Seed Pitch Deck | Raised more / Scaled |
| **REC-024** | Main List (Funded - Success/Alive) | Mentimeter [Pre-seed] | 2014 | `funded` ($500K) — 2014 Pre-Seed Pitch Deck | Alive / Raised more |
| **REC-025** | Main List (Funded - Success/Alive) | StackShare [Pre-seed] | 2015 | `funded` ($300K) — 2015 Pre-Seed Pitch Deck | Raised more / Operating |
| **REC-026** | Main List (Funded - Success/Alive) | Avocode [Seed] | 2015 | `funded` ($650K) — 2015 Seed Pitch Deck | Alive / Acquired |
| **REC-027** | Main List (Funded - Success/Alive) | Almabase [Seed] | 2016 | `funded` (Seed) — 2016 Seed Pitch Deck | Alive / Operating |
| **REC-028** | Main List (Funded - Success/Alive) | CENOS [Pre-seed] | 2020 | `funded` (€312K) — 2020 Pre-Seed Pitch Deck | Raised more / Operating |
| **REC-029** | Main List (Funded - Success/Alive) | Lexop [Pre-seed] | 2017 | `funded` (CA$100K) — 2017 Pre-Seed Pitch Deck | Raised more / Operating |
| **REC-030** | Main List (Funded - Success/Alive) | Ingu Solutions [Pre-seed] | 2016 | `funded` (CA$304.8K) — 2016 Pre-Seed Pitch Deck | Raised more / Operating |
| **REC-031** | Main List (Funded - Success/Alive) | Zestful [Seed] | 2019 | `funded` ($1.2M) — 2019 Seed Pitch Deck | Raised follow-on |
| **REC-032** | Main List (Funded - Success/Alive) | AceUp [Seed] | 2019 | `funded` ($1.7M) — 2019 Seed Pitch Deck | Raised more / Operating |
| **REC-033** | Main List (Funded - Success/Alive) | Foursquare [Seed] | 2009 | `funded` ($1.35M) — 2009 Seed Pitch Deck | Raised more / Operating |
| **REC-034** | Main List (Funded - Success/Alive) | LinkedIn (Dec 11, 2006 BVP Memo) [Series C] | 2006-12-11 | `funded` — Dec 11, 2006 BVP Series C Memo by Jeremy Levine ([BVP Archive](https://www.bvp.com/memos/linkedin); distinct from v3.1 S17) | Raised more / IPO & Acq. |
| **REC-035** | Main List (Funded - Success/Alive) | Shopify (2010 BVP Memo) [Series A] | 2010-11 | `funded` ($7M) — Nov 2010 BVP Investment Memo ([BVP Archive](https://www.bvp.com/memos/shopify)) | Raised more / IPO |
| **REC-036** | Main List (Funded - Success/Alive) | Twilio (2009 BVP Memo) [Seed / Series A] | 2009-11 | `funded` ($3.7M) — Nov 2009 BVP Investment Memo ([BVP Archive](https://www.bvp.com/memos/twilio)) | Raised more / IPO |
| **REC-037** | Main List (Funded - Success/Alive) | Pinterest (2011 BVP Memo) [Series A] | 2011-05 | `funded` ($10M) — May 2011 BVP Investment Memo ([BVP Archive](https://www.bvp.com/memos/pinterest)) | Raised more / IPO |
| **REC-038** | Main List (Funded - Success/Alive) | Twitch / Justin.tv (2012 BVP Memo) [Early] | 2012-08 | `funded` ($15M) — Aug 2012 BVP Investment Memo ([BVP Archive](https://www.bvp.com/memos/twitch)) | Raised more / Acquired |
| **REC-039** | Main List (Funded - Success/Alive) | Uber (UberCab 2008 Seed Deck) [Pre-seed / Seed] | 2008-12 | `funded` ($200K + $1.25M) — 25-slide 2008 Pitch Deck | Raised more / IPO |
| **REC-040** | Main List (Funded - Success/Alive) | Mint.com [Seed] | 2006 | `funded` ($750K) — 2006 Pre-Launch Seed Pitch Deck | Raised more / Acquired |
| **REC-041** | Flagged: Accel. Funded | Dropbox (YC S07) [Pre-seed] | 2007-04 | `funded` — Verbatim YC S07 Written Application ([YC Archive](https://www.ycombinator.com/apply/dropbox)) | Raised more / IPO |
| **REC-042** | Flagged: Accel. Funded | GitLab (YC W15) [Seed] | 2014-11 | `funded` — Verbatim YC W15 Written Application ([YC Archive](https://www.ycombinator.com/companies/gitlab)) | Raised more / IPO |
| **REC-043** | Flagged: Accel. Funded | PostHog (YC W20) [Pre-seed] | 2019-11 | `funded` — Verbatim YC W20 Written Application ([PostHog Handbook](https://posthog.com/handbook/company/story)) | Raised more / Operating |
| **REC-044** | Flagged: Accel. Funded | Per Diem (YC W21) [Pre-seed] | 2020-11 | `funded` — **Weak provenance:** unverified third-party repost (no primary founder/YC link) | Raised more / Alive |
| **REC-045** | Flagged: Accel. Funded | Front (YC S14) [Seed] | 2014-05 | `funded` ($3.1M) — 2014 YC S14 Seed Pitch Deck | Raised more / Scaled |
| **REC-046** | Flagged: Accel. Funded | Mattermost / Spinpunch (YC S12) [Pre-seed] | 2012-04 | `funded` — Verbatim YC S12 Written Application | Alive -> Pivoted & Raised |
| **REC-047** | Flagged: Accel. Funded | Podium (YC W16) [Seed] | 2016-03 | `funded` ($2.2M) — 2016 YC W16 Demo Day Pitch Deck | Raised more / Scaled |
| **REC-048** | Flagged: Accel. Funded | SendGrid (Techstars 2009) [Pre-seed] | 2009 | `funded` ($750K) — 2009 Techstars Seed Pitch Deck | Raised more / IPO & Acq. |
| **REC-049** | Flagged: Accel. Funded (Failed) | Tushky (500 Startups) [Seed] | 2011–2012 | `funded` (~$63K + 500 Startups) — 18-slide 2011 Seed Pitch Deck | Dead |
| **REC-050** | Flagged: Accel. Funded (Failed) | Exec (YC W12) [Seed] | 2012 | `funded` ($3.3M) — 2012 Seed Pitch Deck | Dead (Distressed Sale) |
| **REC-051** | Flagged: Crypto / Token | Coinbase (YC S12 Demo Day) [Seed] | 2012-08-21 | `funded` ($600K–$1M) — Aug 2012 Demo Day Deck + Adam Draper email ([Medium](https://barmstrong.medium.com/the-coinbase-seed-round-pitch-deck-50c8ec91d40b)) | Raised more / IPO |
| **REC-052** | Flagged: Crypto / Token | Alluva [Seed] | 2019 | `funded` (Seed) — 2019 Seed Pitch Deck | Dead |

---

## 6. Option B: Standardized YC Application Benchmark ($N = 100$ — Audited `v2`)

To establish a single-format comparison without mixing slide decks and short-answer forms, Option B tracks **100 Y Combinator applications** (**50 Accepted** vs. **50 Rejected**) across 2005–2025 cohorts, stratified by strict provenance gating:
- **Tier-A ($n = 21$: 19 Accepted, 2 Rejected):** Direct primary-source links to verbatim $T_0$ written applications or audited `v3.1` inputs (`OPTB-001`–`019`, `OPTB-051`, `OPTB-052`). Of these, **4 records** (`OPTB-001` Dropbox, `OPTB-019` PostHog, `OPTB-051` Buffer, `OPTB-052` Edicek) have populated $T_0$ text ready for immediate API execution; **17** await verbatim Q&A text ingestion.
- **Tier-B ($n = 12$: 5 Accepted, 7 Rejected):** Founder-published excerpts / multi-attempt framings (gated until full verbatim $T_0$ Q&A text is verified).
- **Tier-C ($n = 67$: 26 Accepted, 41 Rejected):** Official YC directory (`ycombinator.com/companies`) or `RejectedByYC` cohort leads (gated until verbatim $T_0$ Q&A text is harvested).

### 6.1 Accepted YC Cohort (`OPTB-001` to `OPTB-050` — 50 Rows)

| ID | Startup & Batch | Decision | 3-Yr Outcome | Provenance Tier | Reference Link |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **OPTB-001** | Dropbox (YC S07) | Accepted (1) | Raised more / IPO (1) | Tier-A: Audited v3.1 (S02) [Populated] | [YC Official Archive](https://www.ycombinator.com/apply/dropbox) |
| **OPTB-002** | GitLab (YC W15) | Accepted (1) | Raised more / IPO (1) | Tier-A: Audited v3.1 Input (S03) | [YC Official Profile](https://www.ycombinator.com/companies/gitlab) |
| **OPTB-003** | Mixpanel (YC S09) | Accepted (1) | Raised more / Scaled (1) | Tier-A: Audited v3.1 Input (S04) | [YC Official Profile](https://www.ycombinator.com/companies/mixpanel) |
| **OPTB-004** | Reddit (YC S05) | Accepted (1) | Acquired / IPO (1) | Tier-A: Verbatim Application | [Alexis Ohanian Archive](https://alexisohanian.com) |
| **OPTB-005** | Scribd (YC W10) | Accepted (1) | Raised more / Alive (1) | Tier-A: Verbatim Application | [Scribd Archive](https://www.scribd.com/doc/111078156/Yc-Application) |
| **OPTB-006** | MakeGamesWithUs (YC W10) | Accepted (1) | Raised more / Pivoted (1) | Tier-A: Verbatim Application PDF | [Founder Hosted PDF](https://s3.amazonaws.com/mgwu/YC+GM.pdf) |
| **OPTB-007** | Taazr (YC S10) | Accepted (1) | Acquired / Wound down (1) | Tier-A: Verbatim Application | [Ethan Fast Blog](https://ethanfast.com/2011/10/deconstructing-a-successful-yc-application/) |
| **OPTB-008** | Mattermost / Spinpunch (YC S12) | Accepted (1) | Pivoted & Raised more (1) | Tier-A: Verbatim Application | [Mattermost GitHub](https://github.com/mattermost) |
| **OPTB-009** | The Muse (YC W12) | Accepted (1) | Raised more / Alive (1) | Tier-A: Verbatim Application | [The Muse Blog](https://www.themuse.com/advice/the-muses-successful-application-to-y-combinator-w12) |
| **OPTB-010** | Lollipuff (YC W13) | Accepted (1) | Alive / Bootstrapped (1) | Tier-A: Verbatim Application | [Lollipuff Blog](https://www.lollipuff.com/blog/102/lollipuffs-ycombinator-experience) |
| **OPTB-011** | Apptimize (YC S13) | Accepted (1) | Raised more / Acquired (1) | Tier-A: Verbatim Application | [Nancy Hua Blog](https://nancyhua.com/2014/10/08/successful-y-combinator-s13-application/) |
| **OPTB-012** | One Month (YC S13) | Accepted (1) | Alive / Profitable (1) | Tier-A: Verbatim Application | [Pastebin Text](https://pastebin.com/0SMrXX6M) |
| **OPTB-013** | Standard Treasury (YC S13) | Accepted (1) | Acquired by SVB (1) | Tier-A: Verbatim Application | [Zac Townsend Blog](https://blog.zactownsend.com/our-yc-s13-application) |
| **OPTB-014** | Kash (YC S14) | Accepted (1) | Raised more / Acquired (1) | Tier-A: Verbatim Application | [Kash Blog](https://withkash.com/blog/2015/08/27/applying-to-yc-part-2/) |
| **OPTB-015** | Mimir (YC S15) | Accepted (1) | Acquired by HackerRank (1) | Tier-A: Verbatim Application | [Prahasith Veluvolu Blog](https://prahasith.com) |
| **OPTB-016** | Xendit (YC S15) | Accepted (1) | Raised more / Unicorn (1) | Tier-A: Verbatim Application | [Xendit Blog](https://blog.xendit.co/2015/10/06/xendits-successful-application-to-ycombinator-s15/) |
| **OPTB-017** | Staffjoy (YC Fellowship F1) | Accepted (1) | Shut down within 3 yrs (0) | Tier-A: Verbatim Application | [Staffjoy Blog](https://blog.staffjoy.com/staffjoys-yc-fellowship-application-5771c8a105cd) |
| **OPTB-018** | The Flex Company / Flex (YC S16) | Accepted (1) | Raised more / Alive (1) | Tier-A: Verbatim Application | [MakersClaw Archive](https://makersclaw.com/blog/flex-yc-application-s16) |
| **OPTB-019** | PostHog (YC W20) | Accepted (1) | Raised more / Scaled (1) | Tier-A: Verbatim Application [Populated] | [PostHog Handbook](https://posthog.com/handbook/company/story) |
| **OPTB-020** | Justin.tv / Twitch (YC W07) | Accepted (1) | Pivoted / Acquired by Amazon (1) | Tier-C: YC Profile Lead | [YC Profile](https://www.ycombinator.com/companies/twitch) |
| **OPTB-021** | Wufoo (YC W06) | Accepted (1) | Acquired by SurveyMonkey (1) | Tier-C: YC Profile Lead | [YC Profile](https://www.ycombinator.com/companies/wufoo) |
| **OPTB-022** | Heroku (YC W08) | Accepted (1) | Acquired by Salesforce (1) | Tier-C: YC Profile Lead | [YC Profile](https://www.ycombinator.com/companies/heroku) |
| **OPTB-023** | Disqus (YC S07) | Accepted (1) | Raised more / Acquired by Zeta (1) | Tier-C: YC Profile Lead | [YC Profile](https://www.ycombinator.com/companies/disqus) |
| **OPTB-024** | Airbnb (YC W09) | Accepted (1) | Raised more / IPO (1) | Tier-B: Founder Excerpts | [YC Profile](https://www.ycombinator.com/companies/airbnb) |
| **OPTB-025** | Stripe (YC S09) | Accepted (1) | Raised more / Scaled (1) | Tier-B: Founder Excerpts | [YC Profile](https://www.ycombinator.com/companies/stripe) |
| **OPTB-026** | Zapier (YC S12) | Accepted (1) | Profitable / Bootstrapped (1) | Tier-C: YC Profile Lead | [YC Profile](https://www.ycombinator.com/companies/zapier) |
| **OPTB-027** | Coinbase (YC S12) | Accepted (1) | Raised more / Direct Listing (1) | Tier-B: Demo Day & Excerpts | [YC Profile](https://www.ycombinator.com/companies/coinbase) |
| **OPTB-028** | Gusto / ZenPayroll (YC W12) | Accepted (1) | Raised more / Scaled (1) | Tier-C: YC Directory Lead | [YC Profile](https://www.ycombinator.com/companies/gusto) |
| **OPTB-029** | Exec (YC W12) | Accepted (1) | Distressed sale / Shut down (0) | Tier-C: YC Directory Lead | [YC Profile](https://www.ycombinator.com/companies/exec) |
| **OPTB-030** | DoorDash (YC S13) | Accepted (1) | Raised more / IPO (1) | Tier-B: Founder App & Demo Day | [YC Profile](https://www.ycombinator.com/companies/doordash) |
| **OPTB-031** | Zenefits (YC W13) | Accepted (1) | Raised more / Restructuring (1) | Tier-C: YC Directory Lead | [YC Profile](https://www.ycombinator.com/companies/zenefits) |
| **OPTB-032** | Segment (YC S11) | Accepted (1) | Pivoted / Acquired by Twilio (1) | Tier-B: Founder Excerpts | [YC Profile](https://www.ycombinator.com/companies/segment) |
| **OPTB-033** | Algolia (YC W14) | Accepted (1) | Raised more / Scaled (1) | Tier-C: YC Directory Lead | [YC Profile](https://www.ycombinator.com/companies/algolia) |
| **OPTB-034** | Cruise (YC W14) | Accepted (1) | Acquired by GM (1) | Tier-C: YC Directory Lead | [YC Profile](https://www.ycombinator.com/companies/cruise) |
| **OPTB-035** | Checkr (YC S14) | Accepted (1) | Raised more / Scaled (1) | Tier-C: YC Directory Lead | [YC Profile](https://www.ycombinator.com/companies/checkr) |
| **OPTB-036** | Ginkgo Bioworks (YC S14) | Accepted (1) | Raised more / IPO (1) | Tier-C: YC Directory Lead | [YC Profile](https://www.ycombinator.com/companies/ginkgo-bioworks) |
| **OPTB-037** | Razorpay (YC W15) | Accepted (1) | Raised more / Scaled (1) | Tier-C: YC Directory Lead | [YC Profile](https://www.ycombinator.com/companies/razorpay) |
| **OPTB-038** | Rappi (YC W16) | Accepted (1) | Raised more / Scaled (1) | Tier-C: YC Directory Lead | [YC Profile](https://www.ycombinator.com/companies/rappi) |
| **OPTB-039** | Scale AI (YC S16) | Accepted (1) | Raised more / Scaled (1) | Tier-C: YC Directory Lead | [YC Profile](https://www.ycombinator.com/companies/scale-ai) |
| **OPTB-040** | Brex (YC W17) | Accepted (1) | Pivoted / Raised more (1) | Tier-C: YC Directory Lead | [YC Profile](https://www.ycombinator.com/companies/brex) |
| **OPTB-041** | Retool (YC W17) | Accepted (1) | Raised more / Scaled (1) | Tier-C: YC Directory Lead | [YC Profile](https://www.ycombinator.com/companies/retool) |
| **OPTB-042** | Faire (YC W17) | Accepted (1) | Raised more / Scaled (1) | Tier-C: YC Directory Lead | [YC Profile](https://www.ycombinator.com/companies/faire) |
| **OPTB-043** | OpenSea (YC W18) | Accepted (1) | Raised more / Scaled (1) | Tier-C: YC Directory Lead | [YC Profile](https://www.ycombinator.com/companies/opensea) |
| **OPTB-044** | Deel (YC W19) | Accepted (1) | Raised more / Scaled (1) | Tier-C: YC Directory Lead | [YC Profile](https://www.ycombinator.com/companies/deel) |
| **OPTB-045** | Homejoy (YC S10) | Accepted (1) | Shut down (0) | Tier-C: YC Directory Lead | [YC Profile](https://www.ycombinator.com/companies/homejoy) |
| **OPTB-046** | Shyp (YC S13) | Accepted (1) | Shut down (0) | Tier-C: YC Directory Lead | [YC Profile](https://www.ycombinator.com/companies/shyp) |
| **OPTB-047** | Zirtual (YC W11) | Accepted (1) | Abrupt shutdown (0) | Tier-C: YC Directory Lead | [YC Profile](https://www.ycombinator.com/companies/zirtual) |
| **OPTB-048** | Kicksend (YC S11) | Accepted (1) | Shut down within 3 yrs (0) | Tier-C: YC Directory Lead | [YC Profile](https://www.ycombinator.com/companies/kicksend) |
| **OPTB-049** | Buttercoin (YC S13) | Accepted (1) | Shut down in 2015 (0) | Tier-C: YC Directory Lead | [YC Profile](https://www.ycombinator.com/companies/buttercoin) |
| **OPTB-050** | 99dresses (YC W12) | Accepted (1) | Shut down within 3 yrs (0) | Tier-C: YC Directory Lead | [YC Profile](https://www.ycombinator.com/companies/99dresses) |

### 6.2 Rejected YC Cohort (`OPTB-051` to `OPTB-100` — 50 Rows)

| ID | Startup & Batch | Decision | 3-Yr Outcome | Provenance Tier | Reference Link |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **OPTB-051** | Buffer (YC W11 - Applied late 2010) | Rejected (0) | Raised seed & Scaled >$20M ARR (1) | Tier-A: Audited v3.1 (S01) [Populated] | [Buffer Resource Archive](https://buffer.com/resources/buffers-y-combinator-application/) |
| **OPTB-052** | Edicek (YC S25 - Applied Spring 2025) | Rejected (0) | Alive / Bootstrapped (NaN - <3 yrs) | Tier-A: Verbatim Application [Populated] | [Petr Homoky Blog](https://homoky.cz/blog/my-yc-rejection-full-application) |
| **OPTB-053** | Relate (YC W22 Attempt #5) | Rejected (0) | Accepted S22 & Raised Seed (1) | Tier-B: Founder Framing Reconstruction | [Relate Blog](https://relate.so/blog/six-applications-y-combinator/) |
| **OPTB-054** | Reddit / My Mobile Menu (YC S05) | Rejected (0) | Pivoted to Reddit & Acquired (1) | Tier-B: Founder App & Interview Notes | [YC Official Archive](https://www.ycombinator.com) |
| **OPTB-055** | Replit (YC 2016–2017 Rejections #1–#3) | Rejected (0) | Accepted YC W18 & Scaled (1) | Tier-B: Founder Blog Reconstruction | [Replit Blog](https://replit.com/blog/yc) |
| **OPTB-056** | Clearbit (YC Rejection) | Rejected (0) | Acquired by HubSpot (1) | Tier-C: RejectedByYC Directory Lead | [RejectedByYC](https://rejectedbyyc-ten.vercel.app/) |
| **OPTB-057** | Papermark (YC Rejection) | Rejected (0) | Alive / Open-source SaaS (NaN) | Tier-C: RejectedByYC Directory Lead | [RejectedByYC](https://rejectedbyyc-ten.vercel.app/) |
| **OPTB-058** | Testimonial.to (YC Rejection) | Rejected (0) | Bootstrapped >$1M ARR (1) | Tier-C: RejectedByYC Directory Lead | [RejectedByYC](https://rejectedbyyc-ten.vercel.app/) |
| **OPTB-059** | Dub.co (YC Rejection) | Rejected (0) | Raised Seed & Alive (NaN) | Tier-C: RejectedByYC Directory Lead | [RejectedByYC](https://rejectedbyyc-ten.vercel.app/) |
| **OPTB-060** | Screen Studio (YC Rejection) | Rejected (0) | Bootstrapped & Profitable (NaN) | Tier-C: RejectedByYC Directory Lead | [RejectedByYC](https://rejectedbyyc-ten.vercel.app/) |
| **OPTB-061** | Infisical (YC Pre-W23 Rejection) | Rejected (0) | Accepted YC W23 & Raised Seed (1) | Tier-C: RejectedByYC Directory Lead | [RejectedByYC](https://rejectedbyyc-ten.vercel.app/) |
| **OPTB-062** | Paystack (YC Pre-W16 Rejection) | Rejected (0) | Accepted YC W16 & Stripe Acq. (1) | Tier-B: Founder Reconstruction | [YC Profile](https://www.ycombinator.com/companies/paystack) |
| **OPTB-063** | Webflow (YC 2012 Rejections) | Rejected (0) | Accepted YC S13 & Scaled (1) | Tier-B: Founder Reconstruction | [YC Profile](https://www.ycombinator.com/companies/webflow) |
| **OPTB-064** | Amplitude (YC Pre-W12 Rejection) | Rejected (0) | Accepted YC W12 & IPO (1) | Tier-B: Founder Reconstruction | [YC Profile](https://www.ycombinator.com/companies/amplitude) |
| **OPTB-065** | Substack (YC Pre-W18 Rejection) | Rejected (0) | Accepted YC W18 & Scaled (1) | Tier-B: Founder Reconstruction | [YC Profile](https://www.ycombinator.com/companies/substack) |
| **OPTB-066** | Linear (YC Rejection) | Rejected (0) | Raised Series A/B & Scaled (1) | Tier-C: RejectedByYC Directory Lead | [RejectedByYC](https://rejectedbyyc-ten.vercel.app/) |
| **OPTB-067** | Cal.com (YC Rejection) | Rejected (0) | Raised Seed/Series A & Alive (1) | Tier-C: RejectedByYC Directory Lead | [RejectedByYC](https://rejectedbyyc-ten.vercel.app/) |
| **OPTB-068** | Pillar (YC Rejection) | Rejected (0) | Raised Seed / Alive (1) | Tier-C: Directory Lead (direct URL pending) | [RejectedByYC](https://rejectedbyyc-ten.vercel.app/) |
| **OPTB-069** | Baseten (YC Pre-W20 Rejection) | Rejected (0) | Accepted YC W20 & Series B (1) | Tier-C: RejectedByYC Directory Lead | [YC Profile](https://www.ycombinator.com/companies/baseten) |
| **OPTB-070** | Supabase (YC Pre-S20 Rejection) | Rejected (0) | Accepted YC S20 & Scaled (1) | Tier-C: RejectedByYC Directory Lead | [YC Profile](https://www.ycombinator.com/companies/supabase) |
| **OPTB-071** | Superhuman (YC Rejection) | Rejected (0) | Raised Series A–C & Scaled (1) | Tier-C: RejectedByYC Directory Lead | [RejectedByYC](https://rejectedbyyc-ten.vercel.app/) |
| **OPTB-072** | Loom (YC 2016 Rejection) | Rejected (0) | Acquired by Atlassian ($975M) (1) | Tier-C: RejectedByYC Directory Lead | [RejectedByYC](https://rejectedbyyc-ten.vercel.app/) |
| **OPTB-073** | Notion (YC 2015 Rejection) | Rejected (0) | Raised Series A–C & Scaled (1) | Tier-C: RejectedByYC Directory Lead | [RejectedByYC](https://rejectedbyyc-ten.vercel.app/) |
| **OPTB-074** | Calendly (YC Rejection) | Rejected (0) | Bootstrapped & Growth Equity (1) | Tier-C: RejectedByYC Directory Lead | [RejectedByYC](https://rejectedbyyc-ten.vercel.app/) |
| **OPTB-075** | Airtable (YC 2012 Rejection) | Rejected (0) | Raised Series A–F & Scaled (1) | Tier-C: RejectedByYC Directory Lead | [RejectedByYC](https://rejectedbyyc-ten.vercel.app/) |
| **OPTB-076** | Figma (YC 2012 Rejection) | Rejected (0) | Raised Series A–E & Scaled (1) | Tier-C: RejectedByYC Directory Lead | [RejectedByYC](https://rejectedbyyc-ten.vercel.app/) |
| **OPTB-077** | LeafLink (YC Rejection) | Rejected (0) | Raised Institutional Rounds (1) | Tier-C: RejectedByYC Directory Lead | [RejectedByYC](https://rejectedbyyc-ten.vercel.app/) |
| **OPTB-078** | Plausible Analytics (YC Rejection) | Rejected (0) | Bootstrapped & Profitable (1) | Tier-C: RejectedByYC Directory Lead | [RejectedByYC](https://rejectedbyyc-ten.vercel.app/) |
| **OPTB-079** | Fathom Analytics (YC Rejection) | Rejected (0) | Bootstrapped & Profitable (1) | Tier-C: RejectedByYC Directory Lead | [RejectedByYC](https://rejectedbyyc-ten.vercel.app/) |
| **OPTB-080** | Carrd (YC Rejection) | Rejected (0) | Bootstrapped & Profitable (1) | Tier-C: RejectedByYC Directory Lead | [RejectedByYC](https://rejectedbyyc-ten.vercel.app/) |
| **OPTB-081** | Ghost (YC Rejection) | Rejected (0) | Non-profit Open-Source Alive (1) | Tier-C: RejectedByYC Directory Lead | [RejectedByYC](https://rejectedbyyc-ten.vercel.app/) |
| **OPTB-082** | ConvertKit / Kit (YC Rejection) | Rejected (0) | Bootstrapped >$30M ARR (1) | Tier-C: RejectedByYC Directory Lead | [RejectedByYC](https://rejectedbyyc-ten.vercel.app/) |
| **OPTB-083** | Gumroad (YC Rejection) | Rejected (0) | Raised Seed / Alive (1) | Tier-C: RejectedByYC Directory Lead | [RejectedByYC](https://rejectedbyyc-ten.vercel.app/) |
| **OPTB-084** | Mailchimp (YC Early Rejection) | Rejected (0) | Acquired by Intuit (1) | Tier-C: RejectedByYC Directory Lead | [RejectedByYC](https://rejectedbyyc-ten.vercel.app/) |
| **OPTB-085** | Tally Forms (YC Rejection) | Rejected (0) | Bootstrapped & Profitable (1) | Tier-C: RejectedByYC Directory Lead | [RejectedByYC](https://rejectedbyyc-ten.vercel.app/) |
| **OPTB-086** | Senja.io (YC Rejection) | Rejected (0) | Bootstrapped & Alive (NaN) | Tier-C: RejectedByYC Directory Lead | [RejectedByYC](https://rejectedbyyc-ten.vercel.app/) |
| **OPTB-087** | Midjourney (YC Rejection) | Rejected (0) | Bootstrapped & Scaled (1) | Tier-C: RejectedByYC Directory Lead | [RejectedByYC](https://rejectedbyyc-ten.vercel.app/) |
| **OPTB-088** | Postman (YC Rejection) | Rejected (0) | Raised Series A–D & Scaled (1) | Tier-C: RejectedByYC Directory Lead | [RejectedByYC](https://rejectedbyyc-ten.vercel.app/) |
| **OPTB-089** | HashiCorp (YC Rejection) | Rejected (0) | Raised Series A–E & IPO (1) | Tier-C: RejectedByYC Directory Lead | [RejectedByYC](https://rejectedbyyc-ten.vercel.app/) |
| **OPTB-090** | Cockroach Labs (YC Rejection) | Rejected (0) | Raised Series A–F & Scaled (1) | Tier-C: RejectedByYC Directory Lead | [RejectedByYC](https://rejectedbyyc-ten.vercel.app/) |
| **OPTB-091** | Grafbase (YC Rejection) | Rejected (0) | Raised Seed & Alive (1) | Tier-C: RejectedByYC Directory Lead | [RejectedByYC](https://rejectedbyyc-ten.vercel.app/) |
| **OPTB-092** | Trigger.dev (YC Pre-W23 Rejection) | Rejected (0) | Accepted YC W23 & Seed (1) | Tier-C: RejectedByYC Directory Lead | [YC Profile](https://www.ycombinator.com/companies/trigger-dev) |
| **OPTB-093** | Documenso (YC Rejection) | Rejected (0) | Open-Source SaaS Alive (NaN) | Tier-C: RejectedByYC Directory Lead | [RejectedByYC](https://rejectedbyyc-ten.vercel.app/) |
| **OPTB-094** | Formbricks (YC Pre-S23 Rejection) | Rejected (0) | Accepted YC S23 & Alive (1) | Tier-C: RejectedByYC Directory Lead | [YC Profile](https://www.ycombinator.com/companies/formbricks) |
| **OPTB-095** | Langfuse (YC Pre-W23 Rejection) | Rejected (0) | Accepted YC W23 & Seed (1) | Tier-C: RejectedByYC Directory Lead | [YC Profile](https://www.ycombinator.com/companies/langfuse) |
| **OPTB-096** | Unkey (YC Rejection) | Rejected (0) | Raised Seed & Alive (NaN) | Tier-C: RejectedByYC Directory Lead | [RejectedByYC](https://rejectedbyyc-ten.vercel.app/) |
| **OPTB-097** | Novu (YC Pre-S22 Rejection) | Rejected (0) | Accepted YC S22 & Seed (1) | Tier-C: RejectedByYC Directory Lead | [YC Profile](https://www.ycombinator.com/companies/novu) |
| **OPTB-098** | Tolgee (YC Rejection) | Rejected (0) | Alive / Open-Source (1) | Tier-C: RejectedByYC Directory Lead | [RejectedByYC](https://rejectedbyyc-ten.vercel.app/) |
| **OPTB-099** | Hoppscotch (YC Rejection) | Rejected (0) | Open-Source API Tool Alive (1) | Tier-C: RejectedByYC Directory Lead | [RejectedByYC](https://rejectedbyyc-ten.vercel.app/) |
| **OPTB-100** | Raycast (YC W20 Rejection) | Rejected (0) | Raised Series A & Scaled (1) | Tier-C: RejectedByYC Directory Lead | [RejectedByYC](https://rejectedbyyc-ten.vercel.app/) |

---

## 7. Executable Phase 2 Entity-Blinding & Rubric Evaluator (`option_b_phase2_pipeline_v2.py`)

```python
"""
Option B — Phase 2 (v2): T0 JSON Standardization, Entity-Blinding, and Live LLM Rubric Evaluator
Aligned with:
  - Csaszar, Ketkar, & Kim (2024), Strategy Science (10-Dimension Rubric, 0-100 scale, N=3 runs, T=0.2)
  - Kleinert & Urbig, Startup Evaluations with Generative AI (Blinded vs. Unblinded digital-footprint ablation)
  - Business Economics v3.1 Governance Rules (Strict separation of evaluator inputs from ground-truth labels)
"""

import csv
import json
import os
import re
import time
import urllib.request
from typing import Dict, List, Any

RUBRIC_DIMENSIONS = [
    "team_and_background",
    "execution_plan",
    "financial_feasibility",
    "writing_and_polish",
    "value_proposition_innovativeness",
    "market_opportunity",
    "competitive_moat",
    "customer_need_alignment",
    "roi_potential",
    "long_run_viability"
]

SYSTEM_PROMPT_T0 = """You are an early-stage startup investment analyst evaluating a Y Combinator written application at the exact timestamp of submission (T0).
STRICT TEMPORAL FIREWALL:
- Evaluate ONLY the provided T0 application text.
- Do NOT use any post-T0 knowledge, brand recognition, or retrospective outcome information.
- Score each of the 10 dimensions on an integer scale from 0 to 100.
- Provide a binary admission recommendation (`predicted_accept`: 1 = Accept, 0 = Reject) and an estimated 3-year survival/follow-on financing probability (`predicted_survival_prob`: 0.00 to 1.00).

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
  "predicted_accept": <0 or 1>,
  "predicted_survival_prob": <float 0.0-1.0>,
  "key_risk_flag": "<one concise sentence>"
}"""


def blind_t0_record(
    record: Dict[str, Any],
    company_aliases: List[str],
    founder_names: List[str],
    product_terms: List[str] = None
) -> Dict[str, Any]:
    product_terms = product_terms or []
    rec_id = record["record_id"]
    pitch = json.loads(json.dumps(record["blended_pitch_text"]))
    url_pattern = re.compile(
        r"https?://\S+|www\.\S+|\b[a-zA-Z0-9-]+\.(com|io|org|co|ai|net|cz|so)\b",
        re.IGNORECASE
    )

    def mask_text(text: str) -> str:
        if not text:
            return text
        masked = url_pattern.sub("[URL_REDACTED]", text)
        for alias in sorted(company_aliases, key=len, reverse=True):
            if alias:
                masked = re.sub(rf"\b{re.escape(alias)}\b", f"[{rec_id}_STARTUP]", masked, flags=re.IGNORECASE)
        for idx, fname in enumerate(sorted(founder_names, key=len, reverse=True), start=1):
            if fname:
                masked = re.sub(rf"\b{re.escape(fname)}\b", f"[FOUNDER_{idx}]", masked, flags=re.IGNORECASE)
        for idx, term in enumerate(sorted(product_terms, key=len, reverse=True), start=1):
            if term:
                masked = re.sub(rf"\b{re.escape(term)}\b", f"[PRODUCT_TERM_{idx}]", masked, flags=re.IGNORECASE)
        return masked

    for field_key, field_val in pitch.items():
        if isinstance(field_val, str):
            pitch[field_key] = mask_text(field_val)

    return {
        "record_id": rec_id,
        "evaluation_mode": "blinded_T0",
        "blended_pitch_text": pitch
    }


def make_unblinded_payload(record: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "record_id": record["record_id"],
        "evaluation_mode": "unblinded_T0",
        "blended_pitch_text": record["blended_pitch_text"]
    }


def load_ready_records(jsonl_path: str) -> List[Dict[str, Any]]:
    ready = []
    with open(jsonl_path, "r", encoding="utf-8") as f:
        for line in f:
            if not line.strip():
                continue
            rec = json.loads(line)
            meta = rec.get("meta", {})
            pitch = rec.get("blended_pitch_text", {})
            if (
                meta.get("provenance_tier") == "Tier-A"
                and meta.get("t0_text_status") == "populated_ready"
                and all(isinstance(v, str) and v.strip() for v in pitch.values())
            ):
                ready.append(rec)
    return ready
```