---
kata: 10.W.8
date: 2026-08-01
consumes: 10.W.1, 10.W.2, 10.W.3, 10.W.4, 10.W.5, 10.W.6, 10.W.7
---

# Proposal Pack — Meridian UC1.1 Demand-Driven Inventory Allocation Pilot

---

## Executive Summary

**Meridian's 12% click-&-collect cancellation rate is fixable in 12 weeks — if the root cause is confirmed allocation-driven before a single model line is written.**

EPAM proposes a gated hybrid engagement: a 2-week fixed-fee discovery phase (€33K) that confirms ≥40% of phantom stock is allocation-driven before committing Phase 1–3 budget. If the gate passes, EPAM builds a classical ML allocation model on SAP ECC + POS data with a daily batch cycle, a planner-facing recommendation dashboard with accept/reject capture, and a Prosci-certified change-management track. If the gate fails, Meridian's exposure is €33K — not €340K.

**Three reasons EPAM wins this evaluation:**

1. **Pre-built SAP ECC batch-sync connector.** Deployed at an EU fashion retailer in 2024. Cuts the Forrester benchmark integration timeline (4–6 weeks) to ≤3 weeks — the single largest delivery schedule risk in this RFP. Competitors bid the benchmark; we bid the actuals.

2. **EU AI Act governance out of box.** The 20-pt AI governance criterion is the highest non-technical weight in Meridian's scoring matrix. EPAM's published EU AI Act classification framework — pilot model classified as limited-risk (human-in-loop, Annex III non-applicable) — and standard DPA template are ready to submit. Most competitors write this section from scratch; we fill in the form.

3. **Named team with joint retail delivery history.** RFP §5 criterion 5 explicitly penalises teams that have never worked together. EPAM names [ML Engineer] and [Data Engineer 1] who co-delivered [EU retail allocation project, 2024] — a direct reference against the criterion, not a staffing chart.

**Commercial model.** Phase 0 fixed-fee €33K (discovery gate only) + Phases 1–3 capped T&M at €307K cap = **€340K all-in ceiling**. Within the RFP §4 €250K–€350K envelope. No open-ended T&M (RFP §7 compliant). Change-control triggers are named in the contract, not left as "scope TBD."

**Top risk and mitigation.** Root-cause gate fails (< 40% of phantom stock is allocation-driven). Mitigation: Phase 0 is priced as a bounded fixed-fee gate. If the diagnostic confirms the root cause is operational rather than allocation-driven, the engagement terminates at €33K. Meridian does not pay €307K for a model that cannot move the phantom stock metric.

**Engagement Lead.** [Named EPAM Engagement Lead — EU entity, onshore]. Reference contact: [EU fashion retailer, 2024 SAP ECC allocation deployment] — contact details provided on shortlist notification.

---

## RFP Response Matrix

*Source: RFP §5 evaluation criteria. Self-scores are honest, not maximised. The pre-bid score table submitted with the proposal uses these values.*

| # | Criterion | Weight | Self-score (0–5) | Weighted | How we meet it | Evidence |
|---|-----------|--------|-----------------|----------|----------------|---------|
| 1 | **Technical approach** | 30 | 4 | 120 | Phase 0 root-cause gate with named arbiter (Head of Retail Planning) and 2-day binding ruling window — not a joint-assessment where either party can stall. SAP ECC read-only daily batch via pre-built connector; no write-back. Classical ML on tabular SKU data; explainability layer shows 3 driving signals per recommendation ("move N units of SKU-XXXXX from warehouse A because: stock level 23% of safety stock / lead time 4 days / historical cancellation rate 18% in this SKU×region pair"). Phase 3 measurement methodology: phantom stock rate (baseline vs. pilot-close, reason-code aligned to root-cause classification). | `02-solution.md` §Phases, §Key Assumptions; `04-estimate.xlsx` Effort by Phase; `05-plan.md` M2–M4 |
| 2 | **AI governance / GDPR** | 20 | 5 | 100 | Data classified CLIENT_CONFIDENTIAL under EPAM Data Classification Matrix; stored in EPAM EU-region dev environment; no third-country transfer; no PII in training features (SKU-level tabular data only). EU AI Act classification: limited-risk (automated decision support with human-in-loop accept/reject gate; no Annex III applicability). DPA template submitted with proposal; Prosci sub-contractor data-sharing rider requires Meridian co-signature before Phase 1 start. DIAL and GitHub Copilot both pre-approved on EPAM GenAI allow-list; DIAL used in internal delivery workflow only — not in the production allocation model. | `02-solution.md` §Compliance Shape; `06-ai-native.md` Allow-List Table |
| 3 | **Delivery references** | 20 | 3 | 60 | Reference 1: EU fashion retailer, SAP ECC read-only batch-sync allocation deployment, 2024 — named contact + measurable outcome (phantom stock rate reduction %) provided on shortlist. Reference 2: supply-chain ML deployment with ERP integration, year TBD — to be confirmed before submission. Self-score 3 because second reference is not yet confirmed; if confirmed with SAP history, score rises to 4. | `01-qual-memo.md` Win Theme 1 — **OPEN ITEM OI-2: second reference must be confirmed by 2026-08-21** |
| 4 | **Total pilot cost** | 15 | 4 | 60 | €339,526 all-in (within €250K–€350K envelope). Phase breakdown: Phase 0 €33K fixed / Phase 1 €62K / Phase 2 €159K / Phase 3 €45K / OCM sub-vendor €35K / contingency €22K / margin €37K. Hybrid commercial model (Phase 0 fixed-fee + Phases 1–3 capped T&M) is RFP §7 compliant; no open-ended T&M; change-control triggers named. | `04-estimate.xlsx` Summary tab, Commercial Model tab |
| 5 | **Team composition** | 10 | 4 | 40 | Balanced variant: Engagement Lead (onshore) · Solution Architect (onshore, Phases 0–1) · Data Engineer 1 (nearshore) · Data Engineer 2 (nearshore) · ML Engineer (nearshore) · Project Manager (nearshore) · QA/BI Analyst (nearshore, Phases 2–3). Named ML Engineer and Data Engineer 1 have joint retail delivery history. Availability confirmation pending written sign-off (open item). | `03-staffing.xlsx` Balanced tab — **OPEN ITEM OI-1: named individuals must confirm availability by 2026-08-14** |
| 6 | **Time-to-first-recommendation** | 5 | 3 | 15 | First live planner recommendation target: week 10 of engagement (Dec 1, M4). First model output (internal, non-planner-facing): Phase 2 sprint 2, week 8 (~Nov 14). Backed by Balanced staffing with 1 float week; schedule includes a hard Phase 0 gate that prevents late data-quality discoveries from collapsing the Phase 2 window. | `05-plan.md` M4; `05-timeline.md`; `03-staffing.xlsx` Recommendation tab |
| | **Total** | **100** | — | **395** | Aggregate self-score: 3.95/5 = **79/100** | |

*Score note: the 79/100 aggregate exceeds the RFP §5 "below 60 will not be shortlisted" threshold. The primary scoring risk is criterion 3 (references); confirming a second ERP reference before submission closes the gap.*

---

## Supporting Artefacts — Section References

| Section (RFP §7) | Source file | Key content |
|------------------|-------------|-------------|
| Understanding of Meridian's problem | `00-rfp.md` §2–3 + `01-qual-memo.md` | Root-cause gate framing, 12% baseline, UC1.1 scope |
| Technical approach | `02-solution.md` §Phases, §Key Assumptions, §Client-Side Dependencies | 4-phase delivery with entry/exit criteria; root-cause diagnostic methodology; SAP integration |
| AI governance / GDPR | `02-solution.md` §Compliance Shape; `06-ai-native.md` Allow-List Table | CLIENT_CONFIDENTIAL classification; EU AI Act limited-risk; DPA template; allow-list confirmation |
| Delivery references | `01-qual-memo.md` Win Theme 1 | Named reference (retailer + year + outcome) — see Open Items |
| Proposed team | `03-staffing.xlsx` Balanced tab | Named roles, shore mix, FTE-month ramp profile |
| Delivery plan and milestones | `05-plan.md` §1 Milestone Table; `05-timeline.md` | M0–M5 with entry/exit/owner; Mermaid Gantt; governance rhythm |
| Commercial proposal | `04-estimate.xlsx` Summary tab, Commercial Model tab | Phase-level breakdown; Hybrid model; change-control triggers |
| Pre-bid score table | This document §RFP Response Matrix | All 6 criteria self-scored |
| AI-native delivery | `06-ai-native.md` | Per-phase maturity targets, metrics, allow-list status |

---

## Reconciliation Log

*Every contradiction found between the prior artefacts and its resolution. The pack is reconciled, not stapled.*

### R1 — Executive sponsor mandate date (PATCHED)

**Contradiction.** `05-plan.md` §2.1 Steering Committee stated: "written planner mandate before **2026-11-28** (Phase 2 start − 3 days)." Phase 2 starts 2026-10-28, so the correct deadline is **2026-10-24** (3 business days before Phase 2 start). The date 2026-11-28 falls during Phase 2 week 4 — after the date it purports to be a deadline for.

**Patch.** `05-plan.md` line corrected to: "written planner mandate before 2026-10-24 (Phase 2 start − 3 business days; Phase 2 begins 2026-10-28)."

**Status.** Patched. `04-estimate.xlsx` Assumption Register A3 already had the correct framing ("before Phase 2 week 1"); no patch needed there.

---

### R2 — Contingency rate: 7% in staffing vs. 8% in estimate

**Contradiction.** `03-staffing.xlsx` Balanced variant uses a **7% contingency** (€19,632 on €280K subtotal). `04-estimate.xlsx` uses **8% contingency** (€22,384), sized from the risk register (5 risks × expected value × 2× tail-risk factor = €22,300; 8% of delivery subtotal rounds to €22,384).

**Resolution.** The estimate is the commercially authoritative document. The staffing was a cost-modelling artefact; its contingency was a placeholder rule of thumb. The estimate's 8% is risk-register-sized and therefore the correct rate. The additional ~€2,800 difference is absorbed within the RFP §4 budget envelope (total remains €340K < €350K ceiling).

**Status.** No patch needed in the source files. Documented here for bid-defence preparation: if Meridian challenges the contingency rate, the answer is "sized from named risks × expected value × 2× tail factor — see Risk Register tab."

---

### R3 — "First recommendation in week 6" (staffing) vs. M4 = week 10–11 (plan)

**Contradiction.** `03-staffing.xlsx` Recommendation tab states: "Balanced: First rec: Wk 6." `05-plan.md` M4 places the first live planner recommendation at 2026-12-01, which is week 10–11 of the engagement (5 weeks into Phase 2).

**Resolution.** The staffing language was imprecise. "Week 6" referred to the **first model output** — the date Phase 2 begins and the ML engineer starts producing candidate recommendations internally. The **first live planner-facing recommendation** (dashboard live, planners onboarded, accept/reject capture running) is correctly stated as M4 = Dec 1 = week 10–11. These are two different events. The RFP criterion 6 asks for "earliest week a planner receives a live recommendation" — the answer is week 10 (Dec 1). First internal model output (week 8, ~Nov 14) is noted as context but not the criterion answer.

**Status.** No patch needed; the distinction is clarified here and in the RFP response matrix row 6.

---

### R4 — Pilot close date: 2026-12-15 (plan) vs. 2026-12-19 (RFP §6)

**Contradiction.** `05-plan.md` M5 states pilot close = **2026-12-15** (end of 12 weeks from kick-off). RFP §6 timeline states **"Pilot close and measurement report: 2026-12-19"**.

**Resolution.** These are two different events. The **operational pilot close** (model off, planner sessions ended, artefacts frozen) is 2026-12-15 at the end of 12 calendar weeks. The **measurement report submission deadline** per RFP §6 is 2026-12-19 — 4 additional days for the measurement report to be prepared from the frozen data and submitted to Meridian. The plan's M5 is operational close; report submission on 2026-12-19 is the RFP submission deadline for that document.

**Patch.** `05-plan.md` M5 exit criterion already includes "Phantom stock measurement report" — the date 2026-12-15 should be read as the close of the measurement window, with report submission to Meridian by 2026-12-19 per RFP §6. No structural patch needed; this is clarified here.

**Status.** Documented. Proposal narrative will state "operational pilot close: 2026-12-15; measurement report delivered to Meridian steering committee by 2026-12-19 per RFP §6."

---

### R5 — Staffing cost (€300K) vs. estimate total (€340K): confirmed non-contradiction

**Potential confusion.** `03-staffing.xlsx` Balanced total is ~€300K; `04-estimate.xlsx` total is ~€340K. A reviewer might read this as an inconsistency.

**Resolution.** These represent different things. The staffing total is **cost-to-EPAM** (delivery effort + OCM pass-through + expenses + contingency, with no margin). The estimate total is **price-to-Meridian** (same delivery costs + margin of ~€37K at 11% of revenue — the strategic pilot rate, below the standard 20% margin target). The €40K difference is the margin line, which is a correct and intentional difference between an internal cost model and a client-facing proposal price.

**Status.** Non-contradiction. Documented here so the bid-defence team can answer the "why do the two documents show different totals" question without hesitation.

---

## Open-Items Log

*Every unresolved item going into the bid defence. None of these are hidden — naming them is a discipline signal.*

| # | Item | Blocking? | Owner | Deadline |
|---|------|-----------|-------|----------|
| **OI-1** | Named individuals (ML Engineer, Data Engineer 1) must confirm in writing that they are available for the full 12-week engagement window (2026-09-22 to 2026-12-15). Availability confirmation must be on file before submission. | **Yes — submission blocker** | EPAM Resource Management | **2026-08-14** |
| **OI-2** | Second delivery reference: a supply-chain or retail client with ERP integration history. First reference (EU fashion retailer, 2024 SAP ECC) is confirmed; second reference is TBD. Self-score on criterion 3 rises from 3/5 to 4/5 if confirmed with SAP ECC history. | **Yes — submission risk** (one reference is disqualifying in some procurement panels) | EPAM Account Management | **2026-08-21** |
| **OI-3** | Specific Prosci sub-vendor firm name. Current proposal states "Prosci-certified OCM practice (EU entity) from EPAM pre-qualified panel — specific firm named at contract stage." Meridian's procurement team may require the sub-vendor name at proposal stage, not contract stage. | **No — clarification question** | EPAM Engagement Lead | Written question due 2026-08-07 |
| **OI-4** | Prosci right-to-cure clause in sub-contractor MSA. Flagged in `02-review.md` Critique 2 as a gap: if adoption falls below 30%, EPAM is contractually liable to Meridian but contractually dependent on Prosci to fix it. The right-to-cure clause (≤5 business days to remediate, EPAM may replace Prosci mid-flight) must be drafted into the sub-contractor MSA before contract signature. | **No — pre-contract Legal action** | EPAM Legal | Before contract draft (post-award) |
| **OI-5** | DPA template and sub-contractor data-sharing rider co-signature. EPAM standard DPA submitted with proposal. Meridian Legal must co-sign the data-sharing rider before Phase 1 start. If Meridian Legal review takes > 2 weeks post-award, Phase 1 start date shifts. | **No — timeline risk post-award** | Meridian Legal + EPAM Legal | Before Phase 1 start (by 2026-10-06) |
| **OI-6** | EU AI Act audit trail: the proposal commits to a limited-risk classification. If Meridian's compliance team requires a formal conformity assessment log (not required for limited-risk but sometimes requested in regulated retail), EPAM must produce it within 5 business days of request. Prepare the log template pre-bid in case it is requested at the presentation on 2026-09-08–09. | **No — presentation risk** | EPAM AI Governance lead | By 2026-09-05 (before presentation) |

**Submission blockers.** OI-1 and OI-2 must be resolved before 2026-08-28 12:00 CET. If OI-1 is not resolved, the proposal cannot name the required individuals (RFP §5 criterion 5 and §7 disqualifying condition). If OI-2 produces no second reference by submission, the proposal submits with one confirmed reference and an explicit note in the response matrix.
