---
kata: 1.W.1
date: 2026-07-31
buyer: Meridian Retail Group
project: AI-Driven Demand-Allocation Pilot — UC1.1
---

# Request for Proposal
## AI-Driven Demand Allocation Pilot — UC1.1
### Meridian Retail Group | Issued: 2026-07-31

---

## Section 1 — Buyer & Decision

**Buyer.** Meridian Retail Group, EU fashion omnichannel retailer. Revenue: €2–4B. Footprint: 8 countries, 600 stores, 35% online mix. Procurement contact: Head of Technology Partnerships — [contact details issued to shortlisted bidders].

**Decision this RFP makes.** Meridian is selecting one implementation partner to deliver a 12-week AI pilot (UC1.1: Demand-Driven Inventory Allocation) in 1–2 pilot countries. The pilot must produce evidence to support a full-rollout go/no-go at steering committee. Award is for the pilot only; full-rollout engagement is a separate procurement.

**No-AI baseline.** Planning teams use manual weekly allocation reviews against SAP ECC inventory snapshots. Current click-&-collect cancellation rate: 12%. Benchmark target: ≤5% at pilot close.

---

## Section 2 — Objective

Design, build, and operate a demand-driven inventory allocation model that:

1. Ingests SAP ECC inventory data and historical POS/online sales records (5-year horizon) in daily batch.
2. Produces explainable SKU-level allocation recommendations to planners (format: human-readable, actionable within 48 hours, with stated rationale).
3. Captures planner accept/reject feedback for model improvement.
4. Demonstrates a measurable reduction in the click-&-collect cancellation rate from 12% baseline toward the ≤5% target within the 12-week pilot window.

The pilot is not a proof-of-concept. It is a pilot: real planner workflows, real SKUs, real cancellation data.

---

## Section 3 — Scope

### In scope

| Item | Detail |
|------|--------|
| Demand allocation model | Classical ML on tabular data (no generative AI required in pilot phase) |
| SAP ECC integration | Read-only daily batch sync; no write-back to SAP during pilot |
| Pilot countries | Germany and/or France (final selection at kick-off based on POS data quality audit) |
| Planner-facing interface | Recommendation dashboard with accept/reject/reason capture; browser-based |
| Data quality audit | POS completeness check for pilot countries before model training begins (2-week pre-sprint) |
| Root-cause diagnostic | 2-week diagnostic to confirm ≥40% of phantom stock is allocation/visibility-driven (pass gate before model build) |
| Explainability layer | Per-recommendation rationale ("move N units of SKU-XXXXX from warehouse A because…") |
| Pilot measurement | Weekly phantom-stock rate tracking; planner adoption rate (% recommendations actioned within 48 hrs) |

### Out of scope

- Real-time inference or sub-minute latency
- SAP write-back or automated order placement
- Customer identity resolution or personalised offers (UC2.1, UC2.2)
- Full 8-country rollout
- Mobile infrastructure, load forecasting, or autonomous performance monitoring
- Changes to SAP ECC configuration
- GDPR consent management tooling (Meridian IT owns)

---

## Section 4 — Constraints

| Constraint | Value | Source |
|------------|-------|--------|
| Budget envelope | €250,000–€350,000 all-in for 12-week pilot | Steering committee approval |
| Timeline | Pilot complete within 12 weeks of kick-off | Exec mandate |
| Data residency | All processing within EU (GDPR Art. 44 — no third-country transfer without adequacy decision) | Legal |
| SAP integration | Read-only during pilot; no write-back | IT architecture freeze |
| Planner adoption gate | ≥70% of recommendations actioned within 48 hrs by week 8 | Rollout approval threshold |
| Root-cause gate | Root-cause diagnostic must confirm ≥40% of phantom stock is allocation/visibility-driven before model training begins; if not met, pilot scope changes and Meridian reserves the right to suspend | Programme risk management |
| POS data quality gate | If POS completeness < 80% in both candidate countries, pilot is restricted to the higher-quality country only | Data quality pre-sprint |
| Key personnel | Bidder must name and commit specific individuals (data engineer, ML engineer, PM) — no substitution without Meridian approval | Delivery risk |

---

## Section 5 — Evaluation Criteria

Proposals will be scored against the following criteria. Scores are summed to produce a final weighted score out of 100. Price alone cannot win: a proposal with the lowest price but a score below 60/100 on non-price criteria will not be shortlisted.

| # | Criterion | Weight | What "excellent" looks like |
|---|-----------|--------|-----------------------------|
| 1 | Technical approach | 30 | Model design addresses root-cause gate; SAP integration architecture is read-only and verifiable; explainability layer is planner-operable, not just a log dump; rollback plan for POS data quality failure is explicit |
| 2 | AI governance and GDPR compliance | 20 | Named Data Protection Officer or equivalent; documented data-processing agreement; EU data residency confirmed by architecture diagram; bias/fairness assessment for allocation model described; EU AI Act classification stated |
| 3 | Delivery references | 20 | ≥2 references from retail or supply-chain clients with measurable outcomes (name, contact, year); at least one reference involving an ERP integration (SAP preferred) |
| 4 | Total pilot cost | 15 | Within €250K–€350K envelope; cost broken down by phase (pre-sprint, build, planner rollout, measurement); no ambiguous "T&M overrun" clauses without a cap |
| 5 | Team composition | 10 | Named individuals for data engineer, ML engineer, PM roles with CVs; availability confirmed for the full 12-week window; prior collaboration between named individuals evidenced |
| 6 | Time-to-first-recommendation | 5 | Earliest week a planner receives a live recommendation; shorter is better; must be backed by a credible delivery plan, not a promise |

**Pre-bid score table** (bidder self-assessment — submit with proposal):

| Criterion | Weight | Self-score (0–5) | Weighted contribution |
|-----------|--------|-----------------|----------------------|
| Technical approach | 30 | | |
| AI governance / GDPR | 20 | | |
| Delivery references | 20 | | |
| Total pilot cost | 15 | | |
| Team composition | 10 | | |
| Time-to-first-recommendation | 5 | | |
| **Total** | **100** | | |

Self-scores are not binding on Meridian's evaluation but will be used to surface material gaps between bidder self-assessment and Meridian's scoring.

---

## Section 6 — Timeline

| Milestone | Date |
|-----------|------|
| RFP issued | 2026-07-31 |
| Written questions due | 2026-08-07, 17:00 CET |
| Clarifications published (all bidders simultaneously) | 2026-08-12 |
| Proposals due | 2026-08-28, 12:00 CET |
| Shortlist notification and presentation invitations | 2026-09-05 |
| Bidder presentations (virtual, 60 min each) | 2026-09-08–09 |
| Award notification | 2026-09-12 |
| Pilot kick-off (pre-sprint: data quality audit + root-cause diagnostic) | 2026-09-22 |
| Pilot week 1 (model development start, if root-cause gate passes) | 2026-10-06 |
| Pilot close and measurement report | 2026-12-19 |

Meridian reserves the right to extend any milestone by up to 5 business days without re-issuance.

---

## Section 7 — Submission Rules

**Format.** PDF only. No Word, PowerPoint, or ZIP archives. Single document.

**Page limit.** Maximum 30 pages excluding appendices. Appendices permitted for: CVs (max 2 pages each), reference letters, and the pre-bid score table. Proposals exceeding 30 pages in the main body will be disqualified without scoring.

**Required sections (in order):**
1. Executive summary (max 2 pages)
2. Understanding of Meridian's problem (reference the 12% phantom stock rate and root-cause gate explicitly)
3. Technical approach (including data architecture, model design, SAP integration plan, explainability)
4. AI governance and GDPR compliance statement (EU data residency diagram required)
5. Delivery references (name, contact, outcome, year — minimum 2)
6. Proposed team (named individuals + CVs in appendix)
7. Delivery plan and milestones (Gantt or equivalent; must show pre-sprint and root-cause gate as explicit milestones)
8. Commercial proposal (cost breakdown by phase; fixed-price or capped T&M; no open-ended T&M)
9. Pre-bid score table (self-assessment, all 6 criteria)

**Disqualifying conditions:**
- Missing pre-bid score table
- Missing AI governance / GDPR compliance section
- Open-ended T&M pricing with no cap
- No named individuals for data engineer, ML engineer, PM
- Proposal exceeds 30 pages (main body)
- Received after 2026-08-28 12:00 CET

**Questions.** Submit in writing to [rfp-uc11@meridian-retail.eu] by 2026-08-07 17:00 CET. No verbal questions accepted. Responses published to all registered bidders simultaneously; no bilateral clarifications.

**Registration.** Bidders must register intent to respond by 2026-08-14 to receive clarification addenda. Unregistered bidders may submit but will not receive addenda.
