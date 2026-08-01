---
kata: 10.W.8
date: 2026-08-01
standalone: true
max_pages: 2
---

# Executive Summary — Meridian UC1.1 Allocation Pilot
### EPAM Systems | Proposal submitted 2026-08-28

---

**Meridian's 12% click-&-collect cancellation rate is fixable in 12 weeks — if the root cause is confirmed allocation-driven before a single model line is written.**

EPAM proposes a gated engagement: a 2-week fixed-fee discovery phase (€33K) that confirms ≥40% of phantom stock cancellations are caused by allocation and inventory visibility gaps — not store execution or returns processing failures. Only if that gate passes does EPAM commit Phase 1–3 budget. If it fails, Meridian's exposure is €33K, not €340K.

---

## What We Propose

A classical ML demand allocation model running daily batch on SAP ECC inventory data and 5-year POS/online sales history, producing SKU-level allocation recommendations to planners with per-recommendation rationale ("move N units of SKU-XXXXX from warehouse A because: stock level 23% of safety stock / lead time 4 days / 18% historical cancellation rate in this region"). Planners accept or reject in a browser dashboard; every decision is logged for model improvement and for the Phase 3 adoption measurement report.

The engagement runs 12 weeks across four phases. Change management — resistance handling, adoption tracking, and a named Champion network with protected time — is delivered by a Prosci-certified OCM sub-vendor under EPAM governance, not bolted on as training at the end.

---

## Why EPAM Wins

**SAP ECC integration in ≤3 weeks, not 6.** EPAM deployed a read-only SAP ECC batch-sync connector at an EU fashion retailer in 2024. The Forrester benchmark for SAP integration is 4–6 weeks; EPAM's pre-built connector cuts that to ≤3. The difference is whether Phase 2 model build starts in week 6 or week 10. In a 12-week pilot, that margin is the entire engagement.

**EU AI Act governance answered on day one.** The 20-pt AI governance criterion is the highest non-technical weight in Meridian's scoring matrix. EPAM's EU AI Act classification framework classifies the pilot model as limited-risk (human-in-loop; no Annex III applicability), and our standard DPA template is ready to submit. Most bidders write this section from scratch at proposal time; EPAM fills in the form.

**Named team, proven together.** RFP §5 criterion 5 explicitly penalises teams without shared delivery history. EPAM names [ML Engineer] and [Data Engineer 1] who co-delivered [EU retail allocation project, 2024]. The reference is a direct match to Meridian's engagement, not a volume claim.

---

## Commercial Model

| Phase | Model | Amount |
|-------|-------|--------|
| Phase 0 — Discovery & Gate (2 weeks) | Fixed fee | €33,000 |
| Phases 1–3 — Build, Rollout, Handover (10 weeks) | Capped T&M | €307,000 cap |
| **Total ceiling** | | **€340,000** |

Within RFP §4 €250K–€350K envelope. No open-ended T&M (RFP §7 compliant). Change-control triggers are named in the contract: root-cause gate scope change; POS data restriction to one pilot country. EPAM carries cost risk within the cap; Meridian carries scope-change risk above named triggers.

---

## Top Risk and Its Mitigation

**Risk.** Root-cause gate fails: < 40% of phantom stock cancellations are allocation-driven. The model cannot measurably reduce a metric it does not cause.

**Mitigation.** Phase 0 is a bounded fixed-fee gate. The root-cause diagnostic uses a reason-code classification methodology agreed at kick-off; disputed codes are ruled on within 2 business days by Meridian's Head of Retail Planning (named arbiter, binding ruling, non-re-openable). If the gate fails, the engagement terminates at €33K with a root-cause findings report. Phase 1–3 budget is not committed until the gate passes. The risk is priced and bounded — it does not become a €340K liability.

---

## Engagement Lead and Reference

**Engagement Lead.** [Named EPAM Engagement Lead, EU entity, onshore] — responsible for all client commitments and phase-gate sign-off authority. Available for the Meridian presentation (2026-09-08–09) and throughout the 12-week engagement.

**Reference.** [EU fashion retailer, SAP ECC batch-sync allocation deployment, 2024] — reference contact and measurable outcome provided on shortlist notification.

---

*Full proposal: technical approach · AI governance · delivery plan · milestones · commercial breakdown in the main submission. Pre-bid score table appended.*
