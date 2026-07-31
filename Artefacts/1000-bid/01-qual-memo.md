---
kata: 1.W.2
date: 2026-07-31
rfp: Artefacts/1000-bid/00-rfp.md
bidder: EPAM Systems
---

# Bid Qualification Memo — Meridian UC1.1
### Demand-Driven Inventory Allocation Pilot | Decision required: 2026-08-14

---

## Fit Scores

| Dimension | Score | Rationale |
|-----------|-------|-----------|
| Capability | 4/5 | Strong classical ML + SAP ECC integration practice; retail allocation references exist but must be confirmed EU-specific; explainability layer is native to EPAM's ML Platform accelerator |
| Delivery | 3/5 | 12 weeks is feasible but leaves zero float; root-cause diagnostic and POS audit together consume 4 of those weeks before model build starts; any SAP access delay collapses the plan |
| Commercial | 3/5 | €250–350K at EU onsite rates covers ≈2.5 FTEs for 12 weeks; viable only with a nearshore ML engineer; fixed-price or capped T&M required by RFP — contractually risky against a variable-scope root-cause gate |
| Strategic | 4/5 | Meridian is a referenceable EU fashion logo; pilot win leads to full-rollout procurement (separate award, likely ≥€1.5M); AI governance criterion (20 pts) maps directly to EPAM AI Framework — a scoring advantage |

**Aggregate: 14/20**

---

## Win Themes

1. **SAP ECC read-only integration accelerator.** EPAM's pre-built SAP batch-sync connector (deployed at [reference retailer, 2024]) cuts the 4–6 week Forrester benchmark to ≤3 weeks — the single biggest delivery-schedule risk in this RFP.
2. **EU AI Act governance playbook.** The 20-pt AI governance criterion is the highest non-technical weight. EPAM's published EU AI Act classification framework + DPA template gives an out-of-box answer; most competitors will write this section from scratch.
3. **Named team with joint delivery history.** The RFP explicitly penalises teams that have never worked together. EPAM can name [ML engineer] + [data engineer] who co-delivered [retail allocation project] — a direct reference against criterion 5.

---

## Deal-Breaker

**Fixed-price contract on a variable-scope gate.** The root-cause diagnostic is a contractual trap: if <40% of phantom stock is allocation-driven, Meridian "reserves the right to suspend" — but a fixed-price contract gives EPAM no exit. This must be resolved as a capped T&M with a named change-control clause before submission. If Meridian insists on fixed-price with no scope-change mechanism, no-bid.

---

## Top-Three Risks

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| Root-cause gate fails (< 40% allocation-driven): pilot scope collapses after pre-sprint cost is spent | Medium | High | Price the pre-sprint (diagnostic + data audit) as a separate fixed-fee phase; full pilot is conditional on gate pass — limits exposure to ≈€30K if we walk |
| SAP ECC access delayed by Meridian IT (read-only credentials not provisioned by week 2) | Medium | High | Name SAP access as a contractual dependency with a right-to-pause clock; propose parallel synthetic-data track to keep model work moving |
| Named personnel poached or re-allocated before kick-off (award 2026-09-12, kick-off 2026-09-22 — 10-day gap) | Low | High | Secure hard commitments from both named engineers before submission; name one pre-approved backup per role in the proposal |

---

## Competitive Context

| Competitor | Win theme they will hit | Our counter |
|------------|------------------------|-------------|
| Accenture | "Global retail at scale — we've done 20 SAP allocations" — will cite volume of references to neutralise our named-team advantage | Name the specific reference contact and outcome; volume ≠ recency; our 2024 EU retail reference is more directly comparable than a 2019 global engagement |
| Capgemini | "SAP Gold Partner — lowest integration risk" — will hit criterion 1 (technical approach) and criterion 4 (cost) hard; nearshore rates undercut EPAM on price | Counter on AI governance (criterion 2): Capgemini has no published EU AI Act framework; we score that criterion 4–5 while they score 2–3 |

---

## Recommendation

**Bid with conditions.** Fit is strong on capability and strategic dimensions (14/20 aggregate); the AI governance criterion is a near-free 20 points that most competitors cannot match out-of-box. Two conditions must be resolved before submission is authorised: (1) contract structure must be capped T&M with an explicit scope-change mechanism tied to the root-cause gate — if Meridian insists on fixed-price with no relief clause, this becomes a no-bid; (2) named ML engineer and data engineer with joint retail delivery history must confirm availability for the full 12-week window by 2026-08-14. If both conditions are met, this is a winnable deal at a meaningful strategic price.
