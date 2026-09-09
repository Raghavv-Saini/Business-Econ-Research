# Executive Brief: Proposed Research Paper in Business Economics

**Working Title:** _Can AI Pick Winners? Comparing Large Language Models and Venture Capital Decision-Making Using Historical Startup Outcomes_  
**Discipline:** Business Economics (BE) / Strategic Management  
**Base Paper:** Csaszar, Ketkar, & Kim (2024), _Artificial Intelligence and Strategic Decision-Making: Evidence from Entrepreneurs and Investors_, **Strategy Science**, 9(4):322–345  
**Course Format Benchmark:** `Sources/BE_Research_Grp7.pdf` (6-Section IEEE Standard)  
**Master Plan Source:** `Sources/LLM_vs_VC_research_paper_plan.md`  
**File Location:** `Proposed_Research_Paper_Brief.md`

---

## 1. Executive Summary & Core Research Idea

This paper develops a rigorous empirical and theoretical extension of **Csaszar, Ketkar, and Kim (2024)**.

### The Conceptual Advance

- **Finding of the Base Paper:** In Study 2 of Csaszar et al. (2024), the authors evaluated 138 startup business plans across 137 professional VC and angel investors (541 evaluations) and compared them with GPT-4. They documented a positive correlation of **$r = 0.52$**, establishing that _LLMs evaluate startup strategies similarly to human venture capitalists_.
- **The Core Gap:** In Section 5.1 ("Effects on Performance"), Csaszar et al. explicitly acknowledge that **evaluation similarity does not establish predictive validity or superior capital allocation**. An algorithm can replicate human VC judgment while inheriting all human cognitive biases, herding behavior, and blind spots.
- **Our Extension:** We move from _judgment similarity_ to **realized economic outcomes**:
  > **Do LLM-generated investment decisions predict realized startup performance (survival, follow-on funding, liquidation) better than historical venture capital decisions?**

```text
========================================================================================
BASE PAPER (Csaszar et al., 2024)
Startup Pitch at T0 ──┬──> Human VC Evaluation ──┐
                      │                          ├──> Correlation (r = 0.52)
                      └──> LLM Evaluation ───────┘
                      Question: "Do LLMs evaluate startups similarly to human investors?"
========================================================================================
THIS EXTENSION PAPER
Startup Pitch at T0 ──┬──> Historical VC Decision (Invest / Reject) ──┐
                      │                                                ├──> Predict Realized
                      └──> LLM Reconstructed Decision (T0 only) ───────┤    Startup Outcome
                                                                       │    at T1 / T2
                      ┌────────────────────────────────────────────────┘
                      ▼
Question: "Which decision-maker better predicts actual startup survival, funding, and failure?"
========================================================================================
```

---

## 2. Research Questions & Hypotheses

### Primary Research Question

> **RQ:** Do large language model investment evaluations predict subsequent startup outcomes more accurately than historical venture capital decisions when provided identical information available at the time of investment ($T_0$)?

### Core Hypotheses

1. **$H_1$ (Predictive Parity):** LLM-generated investment evaluations predict subsequent startup survival and follow-on funding at least as accurately as historical human VC decisions.
2. **$H_2$ (Asymmetric Failure Detection — "The Lemon Filter"):** LLMs outperform human VCs in identifying early-stage startups that ultimately fail.  
   _Mechanism:_ LLMs systematically evaluate operational consistency and unit economics without founder halo effects or FOMO.
3. **$H_3$ (Outlier Winner Detection — "The Tacit Knowledge Advantage"):** Human VCs outperform LLMs in identifying extreme power-law winners ("unicorns").  
   _Mechanism:_ Identifying transformative outliers requires tacit information, founder grit assessments, and private channel checks absent from written text.
4. **$H_4$ (Super-Additive Ensembling):** A hybrid decision model combining LLM scoring with human VC judgment produces superior predictive accuracy and capital allocation efficiency than either alone.

---

## 3. Grounding in the 7 Selected Research Papers

To substantiate every theoretical claim, empirical assumption, and econometric design choice, the paper incorporates the **seven curated foundational and frontier studies**:

### 1. Gompers, Gornall, Kaplan, & Strebulaev (2020), _Journal of Financial Economics_

- **Title:** _How Do Venture Capitalists Make Decisions?_
- **Empirical Grounding:** Survey of 885 institutional VCs across 681 firms.
- **Role in Our Paper (Section I & II):** Establishes the institutional reality of VC screening. VCs rank the **management team as the primary determinant of success** (prioritizing the "jockey over the horse") and rely heavily on qualitative gut feel. This provides the theoretical baseline for why human investors are vulnerable to interpersonal bias and founder charisma.

### 2. Kahneman, Sibony, & Sunstein (2021), _Noise: A Flaw in Human Judgment_

- **Theoretical Grounding:** Decomposes decision error into **bias** (systematic deviation) and **noise** (unwanted variability).
- **Role in Our Paper (Section II & III):** Demonstrates that human VC committees suffer from high "occasion noise" (decisions vary by time of day, fatigue, deal sequence, and presentation order). In contrast, LLM scoring exhibits near-zero occasion noise when prompts are standardized, explaining why algorithmic screening serves as a consistent baseline filter.

### 3. Kim, Glaeser, Hillis, Kominers, & Luca (2024), _Strategic Management Journal_

- **Title:** _Decision Authority and Algorithmic Returns_
- **Empirical Grounding:** Multi-department empirical field audit of predictive algorithms and managerial discretion.
- **Role in Our Paper (Section II & V):** Provides the **Principal-Agent economic framework**. Even when algorithms are statistically superior, human managers override them in over 40% of cases to minimize private career risk. In VC, junior partners avoid backing unconventional algorithms because backing an unconventional failure destroys careers, while consensus failures are forgiven.

### 4. Guzman & Stern (2015, _Science_; 2017, _American Economic Review_)

- **Title:** _Where Is Silicon Valley?_ / _Nowcasting and Forecasting the Quality of Entrepreneurship_
- **Empirical Grounding:** Analysis of entrepreneurial quality and growth outcomes using objective attributes at founding.
- **Role in Our Paper (Section III - Methodology):** Provides the **methodological validation for $T_0$ prediction**. Guzman & Stern proved that observable characteristics at the moment of founding reliably predict growth and IPO potential, refuting the claim that early-stage outcomes are completely random noise.

### 5. Mollick (2014), _Journal of Business Venturing_

- **Title:** _The Dynamics of Crowdfunding: An Exploratory Study_
- **Empirical Grounding:** Large-scale empirical study of pitch narratives, goal setting, and commercial fulfillment.
- **Role in Our Paper (Section III - Data Sourcing):** Justifies using open, historical crowdfunding and pitch text platforms (e.g., Republic, Seedrs, Kickstarter). Pitch narrative text, team descriptions, and financial targets at $T_0$ are systematically linked to commercial survival, solving the confidentiality bottleneck of private VC rejections.

### 6. Wang et al. (2025), _arXiv Preprint_

- **Title:** _SSFF: Investigating LLM Predictive Capabilities for Startup Success_
- **Empirical Grounding:** Evaluates LLM reasoning on startup pitches and founder-idea fit.
- **Role in Our Paper (Section III & IV):** Identifies a known technical hazard—**LLM over-prediction bias** (a tendency to assign inflated success probabilities based on prestigious founder resumes). We design our prompt calibration and temperature scaling specifically to correct for this bias.

### 7. Liu et al. (2025), _arXiv Preprint_

- **Title:** _LLM Agents as VC Investors: Predicting Startup Success via RolePlay-Based Collective Simulation_
- **Empirical Grounding:** Multi-agent collective simulation modeling VC investment committees.
- **Role in Our Paper (Section III & V):** Operationalizes Csaszar et al.'s cognitive pillar of **Aggregation**. Instead of a single LLM prompt, we simulate an investment committee (Technical Skeptic, Market Sizing Analyst, Financial Auditor), directly validating Hypothesis $H_4$ (Human-AI Ensembling).

---

## 4. Table 1: Systematic Literature Synthesis Matrix (Section II)

This matrix will be prominently featured in Section II of the final paper, mirroring the format of **Table 1 in `BE_Research_Grp7.pdf`**:

| Study Citation                                           | Empirical Setting & Data                                      | Core Methodological Approach                                 | Key Empirical Findings                                                          | Microeconomic / Cognitive Mechanism                                                    | Specific Role in Our Extension                                                                              |
| -------------------------------------------------------- | ------------------------------------------------------------- | ------------------------------------------------------------ | ------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------- |
| **Csaszar, Ketkar, & Kim (2024)**, _Strategy Science_    | 138 startup plans; 541 VC reviews; 250 angel evaluators.      | RCT (Generation) + 10-Dimension Rubric Scoring (Evaluation). | $r = 0.52$ correlation between LLM and VC scores; +0.14 SD generation boost.    | Relaxes bounded rationality in Search and Representation; raises baseline quality.     | **Primary Anchor Paper:** Establishes evaluation similarity, leaving realized outcome validity unaddressed. |
| **Gompers, Gornall, Kaplan, & Strebulaev (2020)**, _JFE_ | 885 institutional VCs across 681 firms.                       | Comprehensive institutional survey and field audit.          | VCs rank the management team as #1 factor; rely heavily on subjective gut feel. | Soft information vs. hard signals; extreme contract incompleteness.                    | **Human Benchmark:** Defines real-world VC decision criteria and human behavioral vulnerabilities.          |
| **Kahneman, Sibony, & Sunstein (2021)**, _Noise_         | Cross-industry behavioral and institutional audits.           | Statistical variance decomposition of expert judgments.      | Human decision-makers exhibit severe occasion and systemic noise.               | Behavioral inconsistency; cognitive fatigue; sequence effects.                         | **Algorithmic Consistency:** Justifies LLM screening as a zero-noise baseline filter.                       |
| **Kim, Glaeser, Hillis, Kominers, & Luca (2024)**, _SMJ_ | 55 enterprise departments; multi-year algorithmic deployment. | Econometric Policy Evaluation & Override Audits.             | 40%+ override rate; human overrides systematically degrade accuracy.            | Principal-Agent agency costs; managerial career-risk aversion vs. profit maximization. | **Agency Mechanism:** Explains why human VCs may reject algorithmic recommendations.                        |
| **Guzman & Stern (2015, 2017)**, _Science / AER_         | State-level corporate registries and startup cohorts.         | Econometric discrete choice modeling from founding signals.  | $T_0$ observable characteristics accurately forecast growth/IPO outcomes.       | Information signaling; objective observables vs. uncodified noise.                     | **Methodological Precedent:** Confirms $T_0$ observable text contains genuine predictive signals.           |
| **Mollick (2014)**, _Journal of Business Venturing_      | 48,500+ projects; pitch narratives and fulfillment tracking.  | Econometric regression on pitch linguistics and outcomes.    | Pitch text structure, spelling, and team size predict venture survival.         | Crowdsourced due diligence; textual signaling under uncertainty.                       | **Data Justification:** Validates open crowdfunding pitch text as an auditable dataset.                     |
| **Wang et al. (2025)**, _SSFF Preprint_                  | Early-stage startup pitch dataset and founder profiles.       | LLM zero-shot and few-shot classification with prompting.    | LLMs achieve high founder-idea fit but suffer from over-prediction bias.        | Transformer attention to prestige markers; confidence miscalibration.                  | **Prompt Calibration:** Guides temperature scaling to correct for algorithmic optimism.                     |
| **Liu et al. (2025)**, _SimVC Preprint_                  | Multi-agent role-playing investor simulation.                 | LLM agent committee debate and consensus voting.             | Committee debate outperforms single-agent LLM predictions.                      | Information Aggregation; devil's advocacy; perspective diversification.                | **Ensembling Precedent:** Informs our Model 3 (VC + Multi-Agent LLM Committee).                             |

---

## 5. Methodology & Econometric Horse-Race Design

### 5.1 The $T_0$ Information Cutoff

- **Strict Temporal Firewall:** The LLM receives strictly information created at or before decision date $T_0$.
- **Audited Prompting:** Prompt states: _"You are an investment analyst at timestamp $T_0$. Evaluate the following startup using only the provided text. Do not utilize information occurring after this date."_

### 5.2 The 10-Dimensional Scoring Rubric (Csaszar et al., 2024)

The LLM evaluates each business across:

1. Team & Background
2. Execution Plan
3. Financial Feasibility
4. Writing & Polish
5. Value Proposition Innovativeness
6. Market Opportunity
7. Competitive Moat
8. Customer Need Alignment
9. ROI Potential
10. Long-Run Viability

Each dimension is scored 0–100, averaged across $N=3$ runs at temperature $T=0.2$.

### 5.3 Econometric Horse-Race Specifications

We estimate nested and non-nested binary outcome models:

839463\text{logit}\left(\mathbb{P}(\text{Success}_i = 1)\right) = \beta_0 + \beta_1 \text{Score}_{i, \text{LLM}} + \beta_2 \text{Decision}_{i, \text{VC}} + \mathbf{\Gamma}' \mathbf{X}_i + \varepsilon_i839463

- **Model A (Human VC Baseline):** Regress outcome on historical VC decision and control variables.
- **Model B (LLM Baseline):** Regress outcome on continuous LLM score and controls.
- **Model C (Horse-Race):** Joint regression. If $\beta_1 > 0$ and statistically significant, the LLM provides incremental predictive information beyond human VC discretion.
- **Model D (Human-AI Ensemble):** Interaction term $\text{Score}_{i, \text{LLM}} \times \text{Decision}_{i, \text{VC}}$ testing super-additivity.

### 5.4 Simulated Capital Allocation Fund ($1,000,000 Pool)

To ensure the paper speaks to **Business Economics**, we model capital allocation efficiency under power-law returns:

- **Capital Pool:** $1,000,000 deployed across 20 deals ($50,000 per deal).
- **Strategies:** VC-selected portfolio vs. LLM-selected portfolio vs. Consensus portfolio.
- **Economic Metrics:** Portfolio ROI, Net Loss Rate on liquidations, and Capture Rate on top-decile winners.

---

## 6. Structural Mapping to `BE_Research_Grp7.pdf` (6 Sections)

| Section         | Title                                 | Key Contents                                                                                             |
| --------------- | ------------------------------------- | -------------------------------------------------------------------------------------------------------- |
| **Frontmatter** | Title, Authors, Abstract, Index Terms | Quantitative abstract reporting F1, ROC-AUC, Vuong test statistics, and simulated ROI.                   |
| **Section I**   | **INTRODUCTION**                      | Economic importance of venture allocation; VC cognitive noise; Csaszar gap; 3 contributions.             |
| **Section II**  | **LITERATURE REVIEW**                 | Bounded rationality, information economics, decision authority, **Table 1 Synthesis Matrix**.            |
| **Section III** | **METHODOLOGY**                       | Mathematical equations, **Fig. 1 Flowchart**, Table II (Data), Table III (Splits), Rubric, Regressions.  |
| **Section IV**  | **RESULTS & FINDINGS**                | Table XI (Metrics), Table XII (Regressions), Kaplan-Meier Survival Curves, Table XIII (Portfolio ROI).   |
| **Section V**   | **DISCUSSIONS**                       | Data quality artifacts, hard vs. soft info frontier, override paradox, **Practitioner Policy Playbook**. |
| **Section VI**  | **CONCLUSIONS & LIMITATIONS**         | Contamination audits, unobserved due diligence data, future research directions.                         |
| **Backmatter**  | **REFERENCES**                        | Formal numbered citations [1]–[40].                                                                      |
