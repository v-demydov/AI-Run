---
kata: 10.W.7
date: 2026-08-01
consumes: 10.W.2, 10.W.3
inputs: 01-qual-memo.md (win themes), 02-solution.md (phases)
---

# AI-Native Delivery — Meridian UC1.1 Pilot

---

## Maturity Level Definitions

| Level | Label | What it means for this engagement |
|-------|-------|-----------------------------------|
| **L1** | Assisted | AI tools used by individuals on specific tasks; adoption is personal, not enforced; no workflow gate requires AI use; no team-level metric |
| **L2** | Augmented | Defined workflow steps require an AI-assisted draft before human review; adoption is measured per sprint against a denominator; deviations are flagged at retro |
| **L3** | Native | AI output quality drives process improvement; DIAL usage logs reviewed at retro; per-phase metric reported to steering; tool use is a delivery requirement, not a preference |

Targets are set to what the Balanced-variant team (EL, SA, DE×2, MLE, PM, QA) can credibly hit in 12 weeks. Stretch targets are labelled; fantasy targets have been excluded.

---

## Per-Phase AI-Native Table

### Intake — Phase 0, weeks 1–2

| Dimension | Detail |
|-----------|--------|
| **Target maturity** | **L1 by month 1** — root-cause diagnostic is the first analytical task; AI assists reason-code classification drafts; no systematic enforcement yet |
| **Adoption metric** | % of POS cancellation reason codes with an AI-assisted draft classification reviewed before analyst finalisation ÷ total distinct reason codes in 12-month dataset. **Target: ≥80% drafted by week 2.** |
| **Tooling baseline** | EPAM DIAL (model routing, EU-region endpoint) — **pre-approved on EPAM GenAI allow-list**. Used by EPAM Data Engineer 1 to generate draft reason-code mappings from the cancellation taxonomy. GitHub Copilot — **pre-approved** — used for Python scripts automating reason-code extraction from POS export. No client-side AI tooling required at this phase. |
| **Named risk** | DIAL output misclassifies an ambiguous code (e.g. "inter-store transfer lag" classified as store-execution rather than allocation-driven), creating a dispute at the Phase 0 gate. Mitigation: classification logic is submitted to Meridian Data team at kick-off; DIAL output is a draft input to EPAM analyst review, not a final classification. Arbiter (Head of Retail Planning) owns binding ruling. |
| **Measurement source** | Reason-code classification CSV committed to `Artefacts/1000-bid/phase0/` in version control with `ai-draft: true` column per row; DIAL session log (internal EPAM) confirms model calls. |

---

### Plan — Phase 0/Phase 1 boundary, weeks 2–3

| Dimension | Detail |
|-----------|--------|
| **Target maturity** | **L1 by month 1, L2 by month 2** — sprint backlog and acceptance criteria drafting moves to systematic AI-assisted generation by Phase 1 sprint 1; stories without an AI-assisted draft AC are flagged at sprint planning, not blocked |
| **Adoption metric** | % of Phase 1 + Phase 2 sprint stories with a DIAL-assisted draft acceptance criterion reviewed and approved before sprint start ÷ total stories in Phase 1–2 backlog. **Target: ≥75% by sprint 3 (month 2).** |
| **Tooling baseline** | EPAM DIAL — **pre-approved** — used by EPAM PM to generate draft ACs from story descriptions. GitHub Copilot — **pre-approved** — used by MLE for technical task breakdown in model build stories. Jira used for story tracking (no AI integration required; DIAL is used externally to Jira). |
| **Named risk** | AI-drafted ACs are accepted at sprint planning without a domain-quality check. A story for the allocation model feature engineering phase may have syntactically correct but semantically vague ACs ("model produces daily recommendations") that cannot be tested. Mitigation: EPAM SA reviews all model-related ACs before sprint start; QA analyst checks testability before sprint closes. |
| **Measurement source** | Jira stories tagged `ai-assisted-ac`; PM confirms tag at sprint planning; count verified at sprint retro against denominator (total stories closed in sprint). |

---

### Build — Phases 1–2, weeks 3–10

| Dimension | Detail |
|-----------|--------|
| **Target maturity** | **L2 by month 2** — code generation is systematic: every PR for model code and ETL transforms requires a Copilot-assisted draft; L3 by month 3 is a stretch target (DIAL usage logged and reviewed at retro, output quality feeds retrospective action items) |
| **Adoption metric (code)** | % of merged PRs in `model/` and `etl/` directories with a GitHub Copilot-assisted first draft (evidenced by Copilot telemetry flag in PR metadata) ÷ total merged PRs to those directories. **Target: ≥70% by sprint 4 (month 2).** |
| **Adoption metric (SQL transforms)** | % of bronze→silver SQL transforms with a DIAL-assisted draft reviewed by DE before commit ÷ total SQL transform files in `transforms/`. **Target: ≥80% by Phase 1 close (week 5).** |
| **Tooling baseline** | GitHub Copilot — **pre-approved** — for Python model code (feature engineering, training pipeline, inference script). EPAM DIAL — **pre-approved** — for SQL transform drafts (DuckDB CTEs for bronze→silver). No generative AI in the production allocation model itself — classical ML only (this is an explicit compliance commitment in 02-solution.md §Compliance Shape). |
| **Named risk** | Copilot generates syntactically correct but semantically wrong feature transformations (e.g. lag window computed on calendar days instead of business days for a retail context). No model-specific unit test catches the error because the test was also Copilot-generated from the same flawed spec. Mitigation: EPAM SA reviews all feature-engineering transforms against the business definition before Phase 2 model training run; QA analyst maintains a human-authored test for each business-critical feature. |
| **Measurement source** | GitHub PR metadata (Copilot telemetry flag); DIAL session log; directory-scoped PR count from `git log --name-only`. |

---

### Validate — Phase 2 acceptance, weeks 8–10

| Dimension | Detail |
|-----------|--------|
| **Target maturity** | **L2 by month 3** — test case generation for the planner dashboard is systematic; AI-assisted draft test cases are required before QA signs off on a dashboard feature; manual acceptance testing remains human-owned |
| **Adoption metric** | % of dashboard test cases with a DIAL-assisted or Copilot-assisted draft reviewed by QA analyst before execution ÷ total test cases in the Phase 2 test plan. **Target: ≥65% by Phase 2 exit (week 10).** |
| **Tooling baseline** | GitHub Copilot — **pre-approved** — for unit and integration test generation (Python test suite for model inference endpoint). EPAM DIAL — **pre-approved** — for spec-to-test-case mapping (converting acceptance criteria to test scenarios). Manual UAT with planners remains tool-agnostic — QA analyst facilitates, no AI in the session itself. |
| **Named risk** | AI-generated tests mirror the implementation rather than testing intent: Copilot generates tests that pass the exact code path it helped write, leaving semantic edge cases undetected. Coverage metric passes (≥65% AI-assisted) but the accept/reject logic for a SKU at a zero-inventory boundary is never tested. Mitigation: QA analyst authors at least 3 boundary-condition tests per model feature without AI assistance; these are labelled `human-authored` in the test suite and cannot be replaced by AI-generated equivalents without QA sign-off. |
| **Measurement source** | Test plan YAML in version control (`tests/`) with `ai-generated: true` flag per test case; QA analyst verifies boundary-condition label at Phase 2 sprint review. |

---

### Handoff — Phase 3, weeks 11–12

| Dimension | Detail |
|-----------|--------|
| **Target maturity** | **L2 by month 3** — documentation generation is systematic: all sections of the handover checklist have an AI-assisted first draft; human review is required before Meridian IT countersigns |
| **Adoption metric** | % of handover documentation sections with a DIAL-assisted first draft reviewed and accepted by Meridian IT ÷ total sections in the handover checklist. **Target: ≥80% by pilot close (week 12).** |
| **Tooling baseline** | EPAM DIAL — **pre-approved** — for model card generation (populated from training metadata + feature list), runbook drafting, and data dictionary generation. GitHub Copilot — **pre-approved** — for `README.md` and inline code documentation. EPAM PM owns handover checklist; DIAL output is a draft input, not a final deliverable. |
| **Named risk** | AI-generated model cards omit non-obvious operational limitations (e.g. model trained on 5-year historical data degrades for SKUs introduced in the last 6 months — a known cold-start problem). Meridian IT countersigns without a domain expert reviewing the limitations section. Mitigation: EPAM MLE authors the limitations section manually from training evaluation results; QA analyst cross-checks model card against the Phase 3 measurement report before handover sign-off. |
| **Measurement source** | Handover checklist MD committed to `Artefacts/1000-bid/phase3/` with section-level metadata (`ai-draft: true/false`); Meridian IT countersignature on file as Phase 3 exit criterion. |

---

### Learn — Phase 3 retros + post-pilot, weeks 11–12 and beyond

| Dimension | Detail |
|-----------|--------|
| **Target maturity** | **L1 by pilot close, L2 in full-rollout** — retro synthesis is AI-assisted from sprint 1; by Phase 3, DIAL output feeds the full-rollout recommendation pack. L2 requires that adoption-pattern analysis (accept rate, Champion session attendance, rejection reason quality) is synthesised by DIAL before the steering committee sees it. |
| **Adoption metric** | % of retro action items with a DIAL-assisted synthesis from raw session notes reviewed by EPAM EL before committing ÷ total action items raised across all retros. **Target: ≥60% synthesised by retro 3 (month 2), ≥80% by pilot close.** |
| **Tooling baseline** | EPAM DIAL — **pre-approved** — for retro note synthesis (raw notes → themed action items). Adoption dashboard (built in Phase 2) is the source of behavioural metrics for the full-rollout recommendation pack. No third-party survey or analytics platform — all signals come from the dashboard audit log and version-control history. |
| **Named risk** | DIAL retro synthesis surfaces statistically frequent themes but smooths over low-frequency qualitative concerns (e.g. one engineer flags a model fairness question about SKU selection; DIAL groups it under "model quality" and it is lost in the action item). Mitigation: EPAM EL reads raw retro notes in full before accepting the DIAL synthesis; any item labelled `qualitative-concern` by any attendee is escalated to the next steering agenda regardless of frequency. |
| **Measurement source** | Retro notes committed to `Artefacts/` with DIAL synthesis hash; `qualitative-concern` tag count tracked in Jira retro board; EPAM EL confirms review at each retro. |

---

## What Is NOT Automated — Human-Owned Decisions

The AI-native section above describes how DIAL and Copilot accelerate drafting, synthesis, and test generation. It does not describe, imply, or promise the automation of any of the following decisions — these remain human-owned throughout the engagement:

**Phase-gate and commercial decisions.** The Phase 0 root-cause gate pass/fail (whether ≥40% threshold is met, which disputed reason codes the Head of Retail Planning rules on), the Phase 0 sign-off that triggers Phase 1–3 budget, and every subsequent phase exit sign-off are decisions made by named humans with contractual authority. No AI output may substitute for a named human's written approval of a gate.

**Client commitments and scope changes.** Every commitment made to Meridian — including scope changes, change-order pricing, timeline adjustments, and commercial concessions — is authored and approved by the EPAM Engagement Lead. DIAL may draft a change-order document; the Engagement Lead owns every word before it is sent.

**Risk register escalation calls.** Whether a failing DQ check blocks the pipeline or degrades to a warning (Data agent escalation rule), whether a planner adoption shortfall triggers the Prosci right-to-cure clause, and whether an InfoSec concern halts data transfer — these are human-owned decisions. The risk register may be maintained with AI-assisted updates; the escalation call is never delegated to an AI tool.

**Performance and people decisions.** Role allocation changes, utilisation concerns, backup-role activation, and any conversation about team performance are owned by the EPAM Engagement Lead and EPAM Delivery Director. No AI tool has access to personnel data.

**Model metric interpretation and rollout recommendation.** The Phase 3 measurement report interprets phantom stock rate movement against the baseline. DIAL may assist in drafting the narrative; the interpretation — including whether the pilot result warrants a full-rollout recommendation and under what conditions — is written and signed by the EPAM Engagement Lead and presented to Meridian steering as a human recommendation.

---

## Allow-List Confirmation Summary

| Tool | Status | Use in this engagement | Scope restriction |
|------|--------|----------------------|-------------------|
| EPAM DIAL | **Pre-approved (EPAM GenAI allow-list)** | Internal EPAM delivery workflow only: classification drafts, AC drafting, SQL transform drafts, documentation generation, retro synthesis | Not used in production allocation model; EU-region endpoint only; no Meridian data ingested without DPA + data-sharing rider co-signature |
| GitHub Copilot | **Pre-approved (EPAM GenAI allow-list)** | Code generation, test drafting, inline documentation | EPAM dev environment only; no Copilot access to Meridian SAP or POS data |
| No other GenAI tools | — | All other AI tools require pre-approval before use; addition of any tool not on this list constitutes a scope change and requires EPAM Delivery Director sign-off | — |
