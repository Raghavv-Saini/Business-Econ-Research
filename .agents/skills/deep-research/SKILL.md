---
name: deep-research
description: "Multi-source, multi-pass deep research agent for comprehensive technical, academic, and market investigations. Formulates structured hypotheses, queries diverse web and literature sources, triangulates empirical findings, audits citations, and synthesizes publication-grade reports."
---

# Deep Research Agent Skill (Antigravity Native)

The Deep Research skill equips Antigravity agents with autonomous, multi-pass research capabilities designed for complex technical due diligence, academic literature synthesis, and business economics investigations.

---

## 1. Operating Protocol

Execute research across five progressive phases:

### Phase 1: Problem Scoping & Decomposition
- Break down the research topic into **3–5 core research questions (RQs)**.
- Identify the target academic or industry context (e.g., Undergraduate Business Economics with an Information Technology focus).
- Establish clear evaluation criteria: empirical validity, theoretical foundations, contradictory findings, and managerial implications.

### Phase 2: Multi-Source Discovery
Execute parallel and iterative search passes using available tools:
- **Academic & Preprints**: Search for top-tier journal articles (AER, QJE, Management Science, Strategy Science, SMJ) and working papers (NBER, SSRN, arXiv).
- **Empirical Evidence**: Locate field experiments, econometric regressions, randomized controlled trials (RCTs), and case studies.
- **Industry & Market Data**: Extract benchmarks, adoption rates, and economic indices.

### Phase 3: Triangulation & Contradiction Analysis
- Compare findings across sources: Where is there consensus (e.g., zero-marginal-cost ideation, productivity boosts for middle/junior workers)?
- Highlight contradictions and boundary conditions (e.g., performance boosts for top performers vs. declines for bottom performers in field studies; risks outside the jagged technological frontier).

### Phase 4: Synthesis & Structuring
- Structure findings into publication-ready markdown briefs.
- Include executive summaries, comparative taxonomy tables, econometric/formal model breakdowns, and actionable strategic takeaways.

### Phase 5: Verification & Citation Audit
- Verify every inline citation (`[Author et al., Year]`).
- Validate data, percentages, regression coefficients, and sample sizes against original source documents.
- Ensure no hallucinated references or unsubstantiated claims.

---

## 2. Integration with Feynman & Subagents
- For intensive literature searches, delegate exploratory queries to the `research` subagent via `invoke_subagent`.
- Cross-reference with the `feynman` skill for academic peer review and paper-to-theory auditing.
