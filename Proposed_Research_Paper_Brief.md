# Executive Brief: Proposed Research Paper in Business Economics

**Working Title:** *Can AI Pick Winners? Comparing Large Language Models and Venture Capital Decision-Making Using Historical Startup Outcomes*  
**Discipline:** Business Economics (BE) / Strategic Management  
**Base Paper:** Csaszar, Ketkar, & Kim (2024), *Artificial Intelligence and Strategic Decision-Making: Evidence from Entrepreneurs and Investors*, **Strategy Science**, 9(4):322–345  
**Course Format Benchmark:** `Sources/BE_Research_Grp7.pdf` (6-Section IEEE Standard)  
**File Location:** `Proposed_Research_Paper_Brief.md`

---

## 1. Executive Summary & Core Research Idea

This research paper proposes an empirical and theoretical extension of **Csaszar, Ketkar, and Kim (2024)**. 

### The Conceptual Leap
* **What the Base Paper Established:** In Study 2 of Csaszar et al. (2024), the authors compared GPT-4's evaluations of 138 startup business plans with 541 evaluations from 137 professional venture capital and angel investors. They found a positive correlation of **$r = 0.52$**, establishing that *LLMs evaluate startup strategies similarly to human investors*.
* **The Missing Gap in the Base Paper:** As Csaszar et al. explicitly note in their Section 5.1 ("Effects on Performance"), **evaluator agreement does not equal decision quality or firm performance**. An AI can agree with human VCs and still replicate human errors, biases, and missed opportunities.
* **Our Proposed Extension:** We shift the benchmark from **human agreement** to **realized real-world outcomes**:
  > **Do LLM-generated investment decisions predict subsequent startup success or failure better than historical venture capital decisions?**

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
1. **$H_1$ (Predictive Parity / Superiority):** LLM-generated investment evaluations predict subsequent startup survival and follow-on funding at least as accurately as historical human VC decisions.
2. **$H_2$ (Asymmetric Failure Detection — "The Lemon Filter"):** LLMs outperform human VCs in identifying early-stage startups that ultimately fail.  
   *Economic Rationale:* LLMs systematically evaluate operational consistency, unit economics, and competitive crowdedness without the social biases, founder halo effects, and FOMO (fear of missing out) that afflict human investors.
3. **$H_3$ (Outlier Winner Detection — "The Tacit Knowledge Advantage"):** Human VCs outperform LLMs in identifying extreme, power-law winners ("unicorns").  
   *Economic Rationale:* Identifying non-consensus, transformative startups relies heavily on tacit information, uncodified founder grit, and private industry networks that are absent from written text.
4. **$H_4$ (Super-Additive Human-AI Ensembling):** A hybrid decision model combining LLM scoring with human VC judgment produces superior predictive accuracy and capital allocation efficiency than either decision-maker operating in isolation.

---

## 3. Grounding in Business Economics Theory

To ensure this paper is recognized as a contribution to **Business Economics** rather than an applied computer science benchmark, the study is framed through three foundational economic pillars:

1. **Information Economics & Hard vs. Soft Signals (Akerlof, 1970; Gompers et al., 2020):**
   * Early-stage venture capital is characterized by extreme information asymmetry.
   * Startups produce **hard information** (audited financials, pitch deck metrics, market size projections) which LLMs process with zero cognitive fatigue.
   * However, VCs rely heavily on **soft information** (founder charisma, integrity, tacit network references). We test whether codified text alone contains sufficient signal to predict venture viability.
2. **Prediction vs. Judgment Unbundling (Agrawal, Gans, & Goldfarb, 2018, 2024):**
   * AI lowers the marginal cost of **prediction** (forecasting venture survival given historical patterns).
   * **Judgment** (setting payoff matrices, defining fund risk tolerance, pricing liquidation preferences) remains an exclusively human economic function.
3. **Principal-Agent Frictions & Managerial Override (Aghion & Tirole, 1997; Kim et al., 2024):**
   * Human venture partners face asymmetric career risks: backing an unconventional startup that fails damages reputational capital far more than backing a consensus failure ("nobody gets fired for investing in an ex-Google founder").
   * LLMs are free from career-risk apprehension, allowing them to serve as an objective screening mechanism.

---

## 4. Methodology & Experimental Design

### 4.1 Strict Temporal Boundaries (Eliminating Look-Ahead Bias)
The single most critical methodological rule is enforcing the $T_0$ information cutoff:
* **Information Available at $T_0$ (Fed to LLM):** Business plan text, executive summary, founder background up to decision date, stated market size, initial capital requested.
* **Information at $T_1 / T_2$ (Outcome Window — Masked from LLM):** Subsequent funding rounds, acquisition, IPO, revenue trajectory, bankruptcy, shutdown.
* *Prompt Constraint:* The LLM is strictly instructed to act as an investment analyst at timestamp $T_0$, evaluating only the provided text.

### 4.2 Data Sourcing Options
To overcome the challenge that private VC rejections are confidential, we propose three auditable data pathways:
1. **Equity Crowdfunding (Republic / Seedrs / Wefunder / Kickstarter):** Provides complete historical pitch texts from 2017–2020, financial goals, investor funding decisions ($T_0$), and verified 5-year commercial survival/dissolution outcomes ($T_1$).
2. **Curated Shark Tank / Dragon's Den Transcripts:** ~1,200 documented pitches with explicit investor offers/rejections at $T_0$ and 5–10 year tracked business outcomes.
3. **Public Accelerator Batches + Crunchbase Snapshots:** Y-Combinator/Techstars cohorts matched with historical Crunchbase and startup mortality databases.

### 4.3 LLM Evaluation Protocol (Replicating Csaszar et al.)
* The LLM evaluates each startup across **Csaszar's 10 dimensions**:
  1. Team
  2. Execution plan
  3. Financials
  4. Writing clarity
  5. Value proposition innovativeness
  6. Market opportunity
  7. Competitive advantage
  8. Customer needs fit
  9. ROI potential
  10. Long-run viability
* **Scoring & Decision:** Continuous index (0–100) and binary action ($a_i \in \{\text{Invest}, \text{Reject}\}$).
* **Multi-Run Averaging:** $N = 3$ iterations per startup at low temperature ($T = 0.2$) to ensure statistical stability.

### 4.4 Econometric Model & Horse-Race Specification
We estimate a multivariate logistic horse-race model:
835565\text{logit}\left(\mathbb{P}(\text{Success}_i = 1)\right) = \beta_0 + \beta_1 \text{Score}_{i, \text{LLM}} + \beta_2 \text{Decision}_{i, \text{VC}} + \mathbf{\Gamma}' \mathbf{X}_i + \varepsilon_i835565
* **$\beta_1 > 0$ with statistical significance** indicates the LLM captures predictive information uncaptured by historical human decisions.
* **Non-nested Vuong tests** and **McFadden's Pseudo-$R^2$** determine which decision-maker exhibits higher explanatory power.

### 4.5 Economic Portfolio Simulation
Beyond statistical classification metrics (Precision, Recall, ROC-AUC), we simulate an investment fund deploying a **\,000,000 capital pool** across three strategies:
* **Strategy A (VC-Led):** Capital allocated purely to historical human VC selections.
* **Strategy B (LLM-Led):** Capital allocated purely to top-scoring LLM selections.
* **Strategy C (Ensemble):** Capital allocated only when both human and LLM agree (consensus rule) or threshold-gated ($\tau^*$).
* *Metrics:* Total portfolio return multiple, capital lost to write-offs, and allocation efficiency under power-law returns.

---

## 5. Structural Format (Conforming to `BE_Research_Grp7.pdf`)

The final manuscript will strictly mirror the 6-section IEEE structure of the course benchmark:

| Section | Title | Key Contents |
|---|---|---|
| **Frontmatter** | Title, Authors, Abstract, Index Terms | Quantitative abstract highlighting predictive metrics, F1, ROC-AUC, and portfolio returns. |
| **Section I** | **INTRODUCTION** | Venture capital economics, human cognitive bottlenecks, the Csaszar et al. (2024) literature gap, three explicit core contributions, paper roadmap. |
| **Section II** | **LITERATURE REVIEW** | Bounded rationality, AI in strategy, information economics in VC, **Table 1: Systematic Literature Synthesis Matrix** (auditing 5 core studies). |
| **Section III** | **METHODOLOGY** | Mathematical formalization of startup evaluation, **Fig. 1 Flowchart**, Table II (Dataset Characteristics), Table III (Train/Test splits), Csaszar 10-dimension prompt rubric, econometric specifications. |
| **Section IV** | **RESULTS & FINDINGS** | Table XI (Classification Metrics: Accuracy, Precision, Recall, F1, ROC-AUC), Table XII (Econometric Horse-Race Regressions), Kaplan-Meier Survival Curves, Error Analysis (Lemons vs. Unicorns), Table XIII (Portfolio Simulation). |
| **Section V** | **DISCUSSIONS** | Data quality & survivorship artifacts, the Soft vs. Hard information frontier, the Override Paradox in venture funds, **Practical Implications for Venture Capitalists & Corporate Strategists**. |
| **Section VI** | **CONCLUSIONS & LIMITATIONS** | Summary of findings, training data contamination audit (Min-K% Prob / Perplexity), unobserved due diligence data, future research directions. |
| **Backmatter** | **REFERENCES** | 35–40 formal numbered academic references ([1]–[40]). |

---

## 6. Key Contributions to Business Economics

1. **First Empirical Test of AI Strategy Realization:** Extends AI strategy research from *perceived quality* (Csaszar et al., 2024) to *market-verified economic performance*.
2. **Resolution of the Venture Screening Debate:** Demonstrates empirically whether scalable textual analysis can displace or augment human venture capital due diligence.
3. **Optimal Capital Allocation Guardrails:** Translates machine learning scores into economic portfolio returns, proving how human-AI ensembles mitigate downside write-offs while preserving upside exposure.
