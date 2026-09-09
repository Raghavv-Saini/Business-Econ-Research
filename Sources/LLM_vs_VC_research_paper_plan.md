# Research Paper Plan
## Working Title

**Can AI Pick Winners? Comparing LLM and Venture Capital Investment Decisions Using Historical Startup Outcomes**

### Alternative titles
- **Evaluating LLMs as Venture Capital Decision-Makers: Evidence from Historical Startup Outcomes**
- **Human vs. AI in Venture Capital: Do LLM Investment Decisions Predict Startup Success?**
- **From Investor Similarity to Investment Performance: Evaluating LLMs Against Venture Capital Decisions**

---

# 1. Core Research Idea

This paper should extend Csaszar, Ketkar, and Kim (2024), *Artificial Intelligence and Strategic Decision-Making: Evidence from Entrepreneurs and Investors*.

The source paper establishes that LLMs can generate and evaluate entrepreneurial strategies at a level comparable to humans. In its second empirical study, the authors compare LLM evaluations of 138 startup business plans with 541 evaluations from 137 human judges, finding a positive correlation of approximately **0.52** between LLM and investor evaluations. However, this asks whether AI evaluates startups similarly to investors—not whether either decision-maker is actually better at identifying future startup success. fileciteturn2file2 fileciteturn2file3

### The extension

Move the question one step forward:

> **Do LLM investment evaluations predict realized startup outcomes better than historical VC/investor decisions?**

Instead of treating human investor evaluation as the benchmark, use **subsequent real-world startup outcomes as the benchmark**.

### Conceptual progression

```text
SOURCE PAPER

Startup information
        ↓
Human investors ──────┐
                      ├──→ Investor evaluation
LLM ──────────────────┘

Question:
"Do LLMs evaluate startups similarly to investors?"


THIS PAPER

Startup information at T0
        ↓
   ┌────┴────┐
   ↓         ↓
Historical  LLM
VC decision decision
   ↓         ↓
   └────┬────┘
        ↓
Actual startup outcome at T1/T2

Question:
"Which decision-maker better predicts what actually happened?"
```

This directly connects to the source paper's framework linking AI-enabled strategic decision-making to eventual firm performance. The source paper explicitly distinguishes its evidence on strategy generation/evaluation from the downstream question of firm performance. fileciteturn2file9

---

# 2. Research Question

## Primary Research Question

> **Do LLM-generated venture investment decisions predict subsequent startup outcomes better than historical venture capital investment decisions?**

## Secondary Questions

1. Are LLMs better than human investors at identifying startups that eventually fail?
2. Are human investors better than LLMs at identifying extreme winners?
3. Do LLMs and human investors make different types of errors?
4. Does combining LLM and human investor judgments improve prediction?
5. Which startup characteristics are associated with cases where AI outperforms humans?
6. Does the performance gap vary by industry, startup stage, funding environment, or information richness?

---

# 3. Theoretical Contribution

The paper should not be framed simply as:

> "We asked ChatGPT to predict startups."

That would make it an AI benchmark rather than a Business Economics/Strategy extension.

The theoretical contribution should be:

> **The source paper establishes similarity between AI and human strategic evaluation. This study tests whether similarity to human judgment translates into superior prediction of realized economic outcomes.**

The central distinction is:

```text
Judgment similarity ≠ Decision quality

LLM ≈ VC
        ↓
Does NOT imply
        ↓
LLM ≈ VC in predicting startup outcomes
```

The paper therefore shifts the dependent variable from **investor evaluation** to **realized startup performance**.

---

# 4. Link to the Source Paper

Use the source paper as the foundation rather than treating it as background literature.

## Source Paper Finding 1 — Strategy Generation

The source paper experimentally compares entrepreneur-generated and LLM-generated business plans. LLM-generated plans received higher overall evaluations, including higher acceptance and investment likelihood. fileciteturn2file14

## Source Paper Finding 2 — Strategy Evaluation

The source paper compares LLM evaluations with evaluations from experienced VC and angel investors. It uses the same evaluation rubric and finds a correlation of approximately 0.52 between LLM and investor scores. fileciteturn2file2

## Source Paper Limitation

The source paper evaluates whether AI can **generate and evaluate strategies**, but the empirical comparison does not directly establish whether AI-selected firms subsequently perform better.

## Extension

Add the missing outcome layer:

```text
AI / Human evaluation
          ↓
Investment decision
          ↓
Actual startup outcome
```

This allows the study to distinguish **agreement with investors** from **predictive validity**.

---

# 5. Hypotheses

Keep the hypotheses limited and testable.

## H1 — Predictive Performance

> **LLM-generated investment evaluations predict subsequent startup outcomes at least as accurately as historical VC/investor evaluations.**

Compare predictive accuracy using identical startup information.

---

## H2 — Failure Detection

> **LLMs are better than historical VC investors at identifying startups that subsequently fail.**

Rationale: LLMs may systematically process large quantities of textual information and identify inconsistencies, weak market logic, or execution risks that human investors overlook.

---

## H3 — Winner Detection

> **Historical VC investors are better than LLMs at identifying extreme startup winners.**

This is an intentionally competing hypothesis.

Human investors may possess tacit knowledge, networks, industry experience, and information that are difficult to infer from a startup's observable information.

---

## H4 — Human-AI Complementarity

> **Combining LLM and human investor evaluations produces better predictions of startup outcomes than either decision-maker alone.**

This is particularly important because the source paper discusses human-AI ensembles and aggregation as an important direction for future research.

---

# 6. Research Design

## 6.1 Unit of Analysis

The basic unit should be:

> **Startup × investment decision**

Each observation represents a startup at a defined historical point in time.

Example:

| Startup | T0 information | Historical VC decision | LLM decision | Future outcome |
|---|---|---|---|---|
| A | Pitch + team + market | Invest | Invest | Successful |
| B | Pitch + team + market | Invest | Reject | Failed |
| C | Pitch + team + market | Reject | Invest | Successful |
| D | Pitch + team + market | Reject | Reject | Failed |

---

# 7. The Most Important Methodological Rule: T0 Information

## Avoid Look-Ahead Bias

The LLM must receive only information that would have been available to an investor **at the historical decision date**.

For every startup define:

### T0 — Decision Date

Information available:

- Business plan
- Pitch deck
- Founder/team information available at the time
- Industry/market information available at the time
- Funding stage
- Previous funding
- Revenue/traction if publicly available at the time
- Other information that historical investors could realistically access

### T1 — Outcome Window

Information that occurs after T0:

- Subsequent funding
- Acquisition
- IPO
- shutdown
- bankruptcy
- major growth
- survival
- revenue/employee growth where available

The LLM must **never see T1 information when making its decision**.

This is essential. Otherwise the experiment becomes hindsight prediction rather than historical decision reconstruction.

---

# 8. Dataset Construction

## 8.1 Ideal Dataset

Find startups for which all four components can be obtained:

1. Historical startup information
2. Historical VC/investment decision
3. Date of decision
4. Subsequent startup outcome

The dataset should contain both:

- successful startups
- failed startups

Do not construct a dataset consisting only of successful venture-backed firms.

---

# 9. Potential Dataset Structure

Create a master table with fields such as:

```text
startup_id
company_name
industry
country
founding_year
decision_year
startup_stage
funding_round
amount_raised_before_T0
founder_information
team_information
business_description
market_information
traction_information
historical_investment_decision
investor_information
outcome
outcome_date
outcome_type
survival_duration
subsequent_funding
acquisition
ipo
failure
```

Create separate fields for information availability:

```text
information_source
information_date
available_at_T0
```

This will make the information cutoff auditable.

---

# 10. Defining "Success"

Do not use only one arbitrary definition.

Create multiple outcome measures.

## Primary Binary Outcome

```text
Success = 1
Failure = 0
```

But define the threshold carefully.

## Possible Outcome Definitions

### Outcome A — Survival

Did the company remain active after X years?

### Outcome B — Follow-on Funding

Did the startup raise another funding round?

### Outcome C — Major Exit

Did it experience:

- acquisition
- IPO
- major liquidity event

### Outcome D — Failure

Did the startup:

- shut down
- become inactive
- enter bankruptcy
- otherwise cease operations?

### Outcome E — Continuous Performance

Where data permit:

- follow-on funding amount
- valuation
- acquisition value
- revenue growth
- employee growth
- survival duration

Use binary outcomes for the main analysis and continuous/ordinal outcomes as robustness checks.

---

# 11. Historical Human Decision

The human benchmark should ideally represent a **real investment decision**, not merely an investor's hypothetical opinion.

Possible benchmark levels:

### Best

Actual VC investment decision:

```text
VC invested = 1
VC did not invest = 0
```

### Acceptable

Investment committee / accelerator acceptance decision.

### Weaker

Historical investor score or recommendation.

Clearly label which one is being used.

The source paper's second study uses investor scores from business-plan evaluations rather than realized investment outcomes, which is precisely the gap this project aims to address. fileciteturn2file2

---

# 12. LLM Experiment

## 12.1 Freeze the Decision Context

For each startup:

```text
Historical information → Prompt → LLM decision
```

The prompt should explicitly state:

> "Evaluate this startup as an investment opportunity using only the information provided below. Assume you are making the investment decision at the stated historical date. Do not use information about what happened after this date."

Do not include outcome information.

---

# 13. LLM Output

Avoid asking the model only:

> "Will this startup succeed?"

Instead replicate an investment decision process.

Ask the model for:

### A. Investment Score

0–100

### B. Investment Decision

```text
INVEST
REJECT
```

### C. Confidence

0–100

### D. Evaluation Dimensions

Use dimensions inspired by the source paper's rubric:

1. Team
2. Execution plan
3. Financials
4. Writing / clarity
5. Innovation and value proposition
6. Market opportunity
7. Competitive advantage
8. Product/customer fit
9. Investment potential
10. Long-run viability

The source paper itself uses these ten dimensions for LLM and investor evaluations. fileciteturn2file2

---

# 14. Model Strategy

Do not rely on a single LLM run.

For example:

```text
Startup
   ↓
Prompt
   ↓
LLM run 1
LLM run 2
LLM run 3
   ↓
Average score
   ↓
Final LLM investment recommendation
```

This follows the source paper's use of multiple LLM iterations and averaging. fileciteturn2file2

## Better Extension

If resources allow, compare multiple models:

- Model A
- Model B
- Model C

But the **primary paper should remain focused**.

The central comparison is:

```text
Human VC vs LLM
```

not:

```text
GPT vs Claude vs Gemini vs ...
```

---

# 15. Main Experimental Groups

Create three decision-makers.

## Model 1 — Historical VC

Actual historical decision.

## Model 2 — LLM

LLM recommendation using T0 information.

## Model 3 — Human + LLM

A simple ensemble.

Possible rules:

### Majority rule

```text
VC invests + LLM invests → Invest

VC rejects + LLM rejects → Reject

VC invests + LLM rejects → Tie / uncertainty

VC rejects + LLM invests → Tie / uncertainty
```

Or:

### Score average

```text
Combined Score =
0.5 × VC Score +
0.5 × LLM Score
```

If historical VC scores are unavailable, use the human decision as a binary signal.

---

# 16. Core Evaluation Metrics

## Classification Metrics

For each decision-maker calculate:

- Accuracy
- Precision
- Recall
- F1 score
- Specificity
- False-positive rate
- False-negative rate
- ROC-AUC
- PR-AUC

Do not rely on accuracy alone because startup failures/successes may be imbalanced.

---

# 17. Error Analysis

This should be a major part of the paper.

Create:

```text
                    Actual Outcome
                 Success       Failure

Invest            TP            FP
Reject            FN            TN
```

Do this separately for:

```text
VC
LLM
VC + LLM
```

Then ask:

### What does AI get wrong?

- False positives
- False negatives
- overconfidence
- underestimation of unusual businesses

### What do VCs get wrong?

- missed winners
- investments in failures
- industry-specific errors
- stage-specific errors

---

# 18. Economic Evaluation

Because this is a Business Economics paper, go beyond prediction accuracy.

Simulate a hypothetical investment strategy.

Example:

```text
Initial capital = $1,000,000

Strategy A:
Invest according to historical VC decisions

Strategy B:
Invest according to LLM decisions

Strategy C:
Invest according to VC + LLM
```

Then compare:

- number of investments
- number of successful investments
- failures
- capital allocated to winners
- capital allocated to failures
- portfolio return, where valuation/exit data permit

This converts:

> "Who predicts better?"

into:

> "Who allocates scarce investment capital more efficiently?"

That is a much stronger economics question.

---

# 19. Statistical Analysis

## 19.1 Baseline Comparison

Compare:

```text
LLM score vs actual outcome
VC score vs actual outcome
```

Use logistic regression:

```text
Success_i =
β0
+ β1 LLMScore_i
+ Controls_i
+ ε_i
```

and:

```text
Success_i =
β0
+ β1 VCScore_i
+ Controls_i
+ ε_i
```

Then compare predictive performance.

---

# 20. Horse-Race Model

The strongest direct specification is:

```text
Success_i =
β0
+ β1 LLMScore_i
+ β2 VCScore_i
+ Controls_i
+ ε_i
```

Interpretation:

- β1 significant → LLM contains predictive information about future outcomes.
- β2 significant → VC judgment contains predictive information.
- Compare magnitude and predictive contribution.

---

# 21. Controls

Depending on dataset availability:

- industry
- startup age
- funding stage
- funding amount
- geography
- founding year
- market size
- prior funding
- founder experience
- number of founders
- employee count
- economic period

Do not include variables that become known only after T0.

---

# 22. Out-of-Sample Testing

This is critical.

Do not evaluate the LLM only on the same sample used to tune prompts.

Split data chronologically if possible:

```text
Older startups
      ↓
Prompt / methodology development

Later startups
      ↓
Final evaluation
```

A chronological split is particularly attractive because it mimics real investment:

> Make the decision first, observe the future later.

---

# 23. Robustness Checks

At minimum include:

## Robustness 1 — Different outcome definitions

Test:

- failure
- survival
- follow-on funding
- major exit

## Robustness 2 — Different prediction thresholds

Example:

```text
Invest if score ≥ 50
Invest if score ≥ 60
Invest if score ≥ 70
```

## Robustness 3 — Multiple LLM runs

Compare:

```text
single run
vs
average of multiple runs
```

## Robustness 4 — Different models

If feasible.

## Robustness 5 — Information restriction

Compare:

```text
full T0 information
vs
business-plan-only information
```

## Robustness 6 — Industry subsamples

Check whether results differ across sectors.

---

# 24. Key Threats to Validity

The paper should explicitly discuss these.

## 24.1 Look-Ahead Bias

The biggest concern.

Solution:

- timestamp all information
- construct T0 information sets
- exclude post-decision information

---

## 24.2 Training Data Contamination

A modern LLM may have encountered information about old startups.

This is especially important for famous startups.

Possible mitigation:

- use less famous/private startups
- use historical documents
- conduct tests using post-training-cutoff information where appropriate
- clearly distinguish prediction from reconstruction

The source paper itself examines whether LLM-human evaluation correlations remain robust for business plans inside and outside the model's training window. fileciteturn2file4

---

## 24.3 Selection Bias

VC-backed startups are not random startups.

Discuss:

```text
Observed startups
≠
All entrepreneurial ventures
```

---

## 24.4 Survivorship Bias

Do not only collect successful startups.

Intentionally include failures.

---

## 24.5 Outcome Measurement

"Success" is difficult to define.

Use several definitions.

---

## 24.6 Historical VC Information Advantage

Historical VCs may have had access to:

- founder interviews
- private financial information
- customer references
- networks
- proprietary due diligence

If the LLM only sees public documents, the comparison is not:

> "AI vs humans with equal information."

Instead it is:

> "AI using observable historical information vs real-world VC decisions made with potentially richer information."

This limitation must be explicit.

---

# 25. Stronger Experimental Variant

If historical VC scores can be obtained, construct:

```text
                     Prediction
                    ┌──────────────┐
                    │              │
Historical VC ──────┤              │
                    │  Startup     │
LLM ────────────────┤  outcome     │
                    │              │
VC + LLM ───────────┤              │
                    └──────────────┘
```

This allows three-way comparison:

1. Human only
2. AI only
3. Human + AI

The third condition is theoretically valuable because the source paper discusses AI-enabled aggregation and human-AI ensembles as an important avenue for strategic decision-making. fileciteturn2file1

---

# 26. Paper Structure

## 1. Introduction

### Paragraph 1 — Problem

VC decisions involve uncertainty and limited information.

### Paragraph 2 — AI development

LLMs increasingly perform strategic evaluation.

### Paragraph 3 — Existing evidence

Csaszar et al. show that LLMs can generate and evaluate entrepreneurial strategies and that LLM evaluations correlate with experienced investors. fileciteturn2file15

### Paragraph 4 — Gap

Similarity between AI and human judgment does not establish whether either judgment predicts actual startup outcomes.

### Paragraph 5 — Research question

Introduce:

> Can LLMs make investment decisions that better predict subsequent startup outcomes than historical VC decisions?

### Paragraph 6 — Contribution

Explain the shift:

```text
Human-vs-AI similarity
          ↓
Human-vs-AI predictive validity
          ↓
Investment allocation efficiency
```

---

# 27. Literature Review

Organize into four streams.

## 2.1 Strategic Decision-Making

Discuss:

- bounded rationality
- strategic evaluation
- decision quality

Connect to Simon and the source paper.

## 2.2 AI and Strategic Decision-Making

Use Csaszar et al. as the central paper.

Emphasize:

- generation
- evaluation
- search
- representation
- aggregation

The source paper frames AI as potentially expanding the limits of bounded rationality. fileciteturn2file1

## 2.3 Venture Capital Decision-Making

Discuss:

- uncertainty
- information asymmetry
- founder evaluation
- market evaluation
- investor expertise

## 2.4 Prediction vs Judgment

Establish the distinction between:

```text
agreement with expert judgment
```

and

```text
prediction of realized outcomes
```

This becomes the conceptual bridge to the empirical study.

---

# 28. Theory and Hypotheses

Develop a conceptual model:

```text
AI capability
      ↓
Information processing
      ↓
Startup evaluation
      ↓
Investment decision
      ↓
Capital allocation
      ↓
Startup outcome
```

Then explain why AI and human investors may differ.

### AI advantages

- consistent evaluation
- rapid information processing
- scalable analysis
- systematic rubric application
- reduced fatigue

### Human advantages

- tacit knowledge
- relationships
- private information
- contextual understanding
- intuition
- industry networks

This creates theoretically plausible predictions in both directions.

---

# 29. Data and Methodology

## 4.1 Dataset

Explain:

- source
- time period
- number of startups
- inclusion criteria
- exclusion criteria

## 4.2 Historical Information Set

Document exactly what was available at T0.

## 4.3 Human Investment Decision

Define the VC benchmark.

## 4.4 LLM Evaluation Procedure

Document:

- model
- model version
- prompt
- temperature/settings if available
- number of runs
- aggregation procedure

## 4.5 Outcome Variables

Define success/failure and alternative outcomes.

## 4.6 Statistical Model

Present:

- descriptive statistics
- logistic regression
- predictive metrics
- horse-race specification
- portfolio simulation

---

# 30. Results

## 5.1 Descriptive Statistics

Show:

- number of startups
- success/failure distribution
- industries
- stages
- VC investment rate
- LLM investment rate

## 5.2 Human vs LLM Evaluation

Show how frequently they agree.

Example:

```text
VC invests / LLM invests
VC rejects / LLM rejects
VC invests / LLM rejects
VC rejects / LLM invests
```

## 5.3 Predictive Performance

Main table:

| Metric | VC | LLM | VC + LLM |
|---|---:|---:|---:|
| Accuracy | | | |
| Precision | | | |
| Recall | | | |
| F1 | | | |
| ROC-AUC | | | |
| PR-AUC | | | |

## 5.4 Regression Results

Main horse-race table:

| Variable | Model 1 | Model 2 | Model 3 |
|---|---:|---:|---:|
| LLM score | | | |
| VC score | | | |
| Controls | No | Yes | Yes |
| Observations | | | |

## 5.5 Error Analysis

Analyze false positives and false negatives.

## 5.6 Portfolio Simulation

Show whether better prediction translates into better capital allocation.

---

# 31. Discussion

Answer:

### What did we learn?

Possible outcomes:

#### Result A — LLM wins

AI may provide a scalable and relatively consistent screening mechanism.

#### Result B — VC wins

Human tacit knowledge and private information remain important.

#### Result C — They are complementary

This is arguably the most strategically interesting result.

The paper should not be written assuming that AI wins.

The research question must remain open.

---

# 32. Expected Contribution

The paper can make three contributions.

## Contribution 1 — AI and Strategic Decision-Making

Extends evidence from evaluation similarity to realized performance.

## Contribution 2 — Venture Capital

Provides evidence on whether LLM-based screening can identify future startup outcomes.

## Contribution 3 — Human-AI Decision-Making

Tests whether AI should replace investors or complement them.

---

# 33. Limitations

Include:

1. Historical data cannot perfectly reproduce real VC decision environments.
2. LLMs may have training-data exposure to some startups.
3. Historical VCs may possess private information unavailable to the LLM.
4. Startup outcomes are noisy and difficult to measure.
5. Venture returns are highly skewed.
6. Results may vary by model/version.
7. LLM decisions are sensitive to prompts.
8. Historical decisions cannot be randomly assigned.

Do not hide these limitations; they are central to interpreting the results.

---

# 34. Final Conceptual Model

The paper should ultimately tell this story:

```text
                         SOURCE PAPER
                              │
                              ▼
                Can LLMs evaluate strategy?
                              │
                       YES / comparable
                              │
                              ▼
                    ┌─────────────────┐
                    │ THIS EXTENSION  │
                    └─────────────────┘
                              │
                              ▼
             Can LLM evaluations predict outcomes?
                              │
                 ┌────────────┴────────────┐
                 ▼                         ▼
             Historical VC                LLM
                 │                         │
                 └────────────┬────────────┘
                              ▼
                    Actual startup outcome
                              │
                              ▼
                  Compare decision quality
                              │
                              ▼
                 ┌────────────────────────┐
                 │ Capital allocation     │
                 │ efficiency              │
                 └────────────────────────┘
                              │
                              ▼
                    Human + AI ensemble?
```

---

# 35. Work Plan

## Phase 1 — Lock the Research Question

**Deliverables:**

- final research question
- 3–4 hypotheses
- conceptual model
- clear definition of extension

---

## Phase 2 — Literature Review

Build a literature matrix:

| Paper | Topic | Data | Method | Finding | Gap for our paper |
|---|---|---|---|---|---|
| Csaszar et al. | AI + SDM | Startups | Experiments | LLM ≈ humans | No realized outcomes |
| Paper 2 | VC decisions | Startups | Empirical | | |
| Paper 3 | AI prediction | | | | |

Target approximately **15–30 high-quality papers**, with the strongest emphasis on strategy, entrepreneurship, VC, AI decision-making, and prediction.

---

## Phase 3 — Dataset Discovery

Before writing the methodology, confirm that the required dataset actually exists.

The minimum viable dataset is:

```text
Startup
+
T0 information
+
Historical investment decision
+
Future outcome
```

Do not proceed with the full paper until this is feasible.

---

## Phase 4 — Data Engineering

Create:

```text
raw/
├── startup_data
├── investor_data
├── historical_documents
└── outcomes/

processed/
├── startup_master.csv
├── t0_information.csv
├── vc_decisions.csv
└── outcomes.csv
```

Every observation should have a clear T0 timestamp.

---

## Phase 5 — LLM Experiment

1. Freeze dataset.
2. Freeze information cutoff.
3. Create standardized prompt.
4. Run LLM multiple times.
5. Save raw outputs.
6. Convert outputs into structured scores.
7. Aggregate runs.
8. Generate final decisions.

Keep the exact prompts and outputs for reproducibility.

---

## Phase 6 — Statistical Analysis

Run analyses in this order:

```text
1. Descriptive statistics
2. VC vs LLM agreement
3. Confusion matrices
4. Classification metrics
5. Logistic regressions
6. Horse-race regression
7. Ensemble model
8. Portfolio simulation
9. Robustness checks
```

---

## Phase 7 — Write the Paper

Recommended order:

```text
Methodology
      ↓
Results
      ↓
Literature Review
      ↓
Theory / Hypotheses
      ↓
Introduction
      ↓
Discussion
      ↓
Abstract
```

Writing the introduction last helps ensure that the claims accurately reflect the results.

---

# 36. Minimum Viable Paper

If data availability becomes difficult, reduce the scope rather than abandoning the idea.

### MVP

```text
Historical startup dataset
+
T0 business information
+
historical investment decision
+
binary outcome
+
one LLM
+
VC vs LLM prediction metrics
```

This is enough for a coherent empirical paper.

### Strong Version

```text
MVP
+
multiple outcome definitions
+
multiple LLM runs
+
horse-race regression
+
industry heterogeneity
+
portfolio simulation
```

### Excellent Version

```text
Strong Version
+
multiple LLMs
+
VC score data
+
human-AI ensemble
+
temporal out-of-sample validation
+
training-data contamination analysis
+
economic return simulation
```

---

# 37. What NOT to Do

### Do not:

- ask the LLM about a startup using today's information
- include future funding/outcome information in the prompt
- evaluate only successful startups
- treat LLM agreement with VCs as proof of superiority
- use accuracy as the only metric
- assume AI will outperform humans
- compare many models without a theoretical reason
- make the paper primarily about prompt engineering
- hide data-selection limitations
- claim causal effects from historical observational data

### The central distinction

```text
Correlation with VC judgment
              ≠
Predictive accuracy
              ≠
Economic return
              ≠
Causal impact of AI
```

The paper should be very precise about which of these it actually identifies.

---

# 38. Final Research Statement

The cleanest version of the project is:

> **This study extends Csaszar, Ketkar, and Kim (2024) by moving from the question of whether LLM evaluations resemble those of experienced investors to whether LLM-generated investment decisions predict realized startup outcomes. Using historical startup information available at the time of investment, we reconstruct investment decisions using an LLM and compare its predictions with historical VC decisions. We then evaluate both decision-makers against subsequent startup outcomes and examine whether combining human and AI judgments improves investment performance.**

That is the core paper. Everything else should support this question.
