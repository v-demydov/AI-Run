---
kata: 10.W.3
date: 2026-07-31
rfp: Artefacts/1000-bid/00-rfp.md
qualification: Artefacts/1000-bid/01-qual-memo.md
compliance_shape: RFP-led (greenfield bid)
---

# Solution Outline — Meridian UC1.1 Demand-Driven Inventory Allocation Pilot

---

## High-Level Approach

EPAM will deliver a demand-driven inventory allocation pilot in three bounded sprints preceded by a mandatory discovery gate: a 2-week pre-sprint that confirms the root cause of phantom stock is allocation-driven (≥40% threshold) and that POS data completeness is sufficient for model training (≥80%). Only if both gates pass does the engagement move to build. The allocation model uses classical ML on tabular SAP/POS data with a daily batch cycle; no real-time inference and no generative AI. Planner-facing output is a recommendation dashboard with SKU-level rationale and accept/reject capture. Change management and planner adoption — the single highest-risk non-technical dependency in this engagement — are delivered by a named OCM sub-vendor (Prosci-certified practice) under EPAM programme governance.

---

## Phases

| Phase | Entry criteria | Exit criteria | Duration | Owner role |
|-------|---------------|---------------|----------|------------|
| **Phase 0 — Discovery & Gate** | Contract signed; SAP read-only credentials committed in writing by Meridian IT; executive sponsor named | Root-cause diagnostic confirms ≥40% of phantom stock is allocation/visibility-driven. Methodology: EPAM classifies each POS cancellation reason code from the most recent 12-month period in the pilot country into (A) allocation/visibility-driven (out-of-stock at source warehouse, incorrect inventory position, inter-store transfer lag) or (B) operational/other (store execution failure, returns processing error, shrinkage, customer cancellation). Classification logic submitted to Meridian Data team at Phase 0 kick-off. Disputed codes escalated to Meridian Head of Retail Planning for a binding ruling within 2 business days; final gate assessment uses the agreed classification with no further dispute mechanism. POS completeness ≥80% in ≥1 pilot country. Written sign-off from Meridian Programme Director on Phase 0 findings report within 3 business days of delivery — if not received in 3 business days, sign-off is deemed granted. | 2 weeks | EPAM Engagement Lead |
| **Phase 1 — Data Foundation** | Phase 0 exit criteria met; pilot country confirmed; SAP read-only credentials provisioned to EPAM dev environment | Bronze dataset (SAP inventory + POS/online sales, 5-year horizon) loaded to EPAM dev environment; data quality report signed off by Meridian Data team; model training baseline agreed (target metric: phantom stock rate, measurement methodology confirmed); Prosci sub-vendor engagement kick-off complete | 3 weeks | EPAM Data Engineer (lead) |
| **Phase 2 — Model Build & Planner Interface** | Phase 1 exit criteria met; ≥5 named planners committed by Meridian for pilot; Prosci adoption workstream active | Allocation model producing daily SKU-level recommendations; planner dashboard live in pilot country with accept/reject/reason capture; ≥5 planners completed onboarding; first-week recommendation accept rate ≥30% (evidence: dashboard audit log) | 5 weeks | EPAM ML Engineer (lead) |
| **Phase 3 — Measurement & Handover** | Phase 2 exit criteria met; ≥4 weeks of live recommendation data collected | Phantom stock rate measurement report (baseline vs. pilot-close, methodology auditable); planner adoption rate documented (% recommendations actioned within 48 hrs, target ≥70%); full-rollout recommendation pack delivered to Meridian steering committee; model artefacts and documentation handed to Meridian IT | 2 weeks | EPAM PM (lead) |

**Total: 12 weeks**

---

## Outsourced Capability — Change Management & Planner Adoption

**Why outsourced.** EPAM has no certified OCM practice. Gate 6 of the opportunity brief explicitly names regional planner resistance as the adoption risk that could sink an otherwise-correct model. Outsourcing to a specialist is lower risk than staffing an OCM generalist from EPAM delivery.

**Sub-vendor.** Prosci-certified OCM practice (EU entity, specific firm to be named at contract stage; EPAM has a pre-qualified panel). Sub-vendor agreement governed by EPAM's standard sub-contractor MSA; client data does not flow to sub-vendor without Meridian co-signature on a data-sharing rider.

| Item | Detail |
|------|--------|
| **What they deliver** | Stakeholder mapping; planner readiness assessment (end of Phase 0); adoption communication plan; 2× facilitated planner workshops (Phase 2, weeks 1 and 3); adoption measurement report (Phase 3) |
| **Integration point** | Sub-vendor deliverables are reviewed and accepted by EPAM Engagement Lead before being presented to Meridian; sub-vendor does not have a direct contractual relationship with Meridian |
| **Governance gate** | EPAM Engagement Lead holds weekly 30-min check-in with sub-vendor lead; escalation path: sub-vendor lead → EPAM Engagement Lead → EPAM Delivery Director (named individual); sub-vendor cannot extend scope or communicate scope changes to Meridian without EPAM sign-off |
| **Evidence required at Phase 2 exit** | Attendance list for both planner workshops; readiness survey results (before and after); first-week accept-rate log (≥30% — owned by sub-vendor OCM track, verified by EPAM dashboard audit) |
| **Remediation if adoption falls below 30% after workshop 1** | Sub-vendor repeats facilitation with Meridian executive sponsor involvement; EPAM Engagement Lead escalates to Meridian Programme Director within 24 hours; if ≥70% adoption rate is not achieved by week 8, the Phase 3 measurement report states this explicitly and the full-rollout recommendation is conditional |

---

## Key Assumptions

| # | Assumption | Consequence if false |
|---|-----------|----------------------|
| A1 | Meridian IT provisions SAP read-only credentials to EPAM dev environment by Day 5 of Phase 0 | Right-to-pause clock starts; Phase 1 start date shifts day-for-day; no cost to EPAM for the delay |
| A2 | Root-cause diagnostic confirms ≥40% of phantom stock is allocation/visibility-driven | Phase 1+ is not initiated; EPAM invoices for Phase 0 only (fixed-fee, ≈€28K); scope change requires written amendment |
| A3 | POS completeness ≥80% in ≥1 pilot country (Germany or France) | Pilot is restricted to the higher-quality country; if both fail, engagement pauses pending Meridian data remediation |
| A4 | ~~Moved to Client-Side Dependencies — see below~~ | (Removed from assumptions; reframed as a hard dependency after adversarial review) |
| A5 | Meridian commits ≥5 named planners (minimum 2 hrs/week for review sessions and workshops) | Phase 2 exit criterion is at risk; EPAM cannot manufacture planner participation |
| A6 | EPAM daily rates based on nearshore ML engineer (Poland/Hungary entity); switch to onshore triggers a change order | Commercial exposure; fixed-price envelope may be breached without a signed amendment |

---

## Client-Side Dependencies

- SAP ECC read-only credentials provisioned by Day 5 (hard dependency)
- POS data extract from pilot-country IT systems (format: CSV or API; agreed at Phase 0 kick-off)
- **Executive sponsor:** named individual with authority to mandate planner participation; commits to ≥1 fortnightly 60-minute steering call throughout Phase 2; written mandate to pilot planners issued before Phase 2 start (hard dependency — Phase 2 cannot begin without written mandate on file)
- Finance-validated order volume and churn rate (for phantom stock measurement baseline — see opportunity brief §3)
- Meridian Programme Director available for weekly 60-min steering calls throughout engagement
- Legal sign-off on EPAM's DPA and sub-contractor data-sharing rider before Phase 1 start

---

## Out of Scope

Everything in RFP §3 out-of-scope list, plus: change management strategy definition (Prosci sub-vendor delivers execution, not strategy — strategy must be agreed by Meridian); full-rollout implementation and 8-country expansion; permanent model hosting or MLOps post-pilot; GDPR consent management tooling; SAP write-back or automated order placement; any use case other than UC1.1.

---

## Compliance Shape

**Shape: RFP-led (greenfield bid) — default EPAM pre-approved tooling.**

| Item | Commitment |
|------|-----------|
| AI tooling | EPAM DIAL (model routing) + GitHub Copilot (code generation) — both on EPAM pre-approved list; no client-side AI tooling required |
| No generative AI in pilot deliverable | Classical ML only; DIAL is not used in the production allocation model — only in internal EPAM development workflow |
| Data classification | SAP inventory + POS data classified CLIENT_CONFIDENTIAL under EPAM Data Classification Matrix; stored in EPAM EU-region dev environment; no third-country transfer |
| DPA | EPAM standard DPA template submitted with proposal; sub-contractor data-sharing rider requires Meridian co-signature before Phase 1 start |
| DPO review trigger | Not triggered for pilot (no PII/PHI in model training features — SKU-level tabular data only); DPO review required if scope expands to customer-level data (UC2.1/UC2.2) |
| EU AI Act classification | Pilot model classified as limited-risk AI system (automated decision support with human in the loop — planner accept/reject gate); no high-risk classification under Annex III |
