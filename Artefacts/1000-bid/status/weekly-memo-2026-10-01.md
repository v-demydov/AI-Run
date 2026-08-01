---
engagement: Meridian UC1.1 Pilot
week: Phase 0 Week 2
memo_date: 2026-10-01
phase_0_gate: 2026-10-06 (5 days)
author: delivery-pm-meridian skill
---

# Weekly Delivery-Health Memo — 2026-10-01

## RAG Status by Workstream

| Workstream | Status | Signal | Source |
|-----------|--------|--------|--------|
| SAP ECC credentials | 🔴 **RED** | Credentials NOT received. Day 7 of 5-day window (deadline was 2026-09-29). Right-to-pause clock is running per Assumption A1 — this is a contractual event, not an advisory flag. Meridian IT has not provided a timeline. | MERID-004 (BLOCKED) |
| Root-cause diagnostic | 🟡 **AMBER** | 14/16 reason codes classified. 2 codes disputed: "inter-store transfer lag" and "order cancellation — supplier OOS". Arbiter ruling (Head of Retail Planning) due 2026-10-02. Final root-cause % cannot be confirmed until ruling. | MERID-001, MERID-006 |
| POS completeness — Germany | 🟢 **GREEN** | 84.2% completeness. Gate criterion (≥80%) met. Germany confirmed as pilot country. | MERID-002 (DONE) |
| POS completeness — France | 🟡 **AMBER** | 71% completeness (preliminary). Below the 80% gate. France will likely be excluded from pilot scope. Meridian Programme Director has not yet formally acknowledged Germany-only scope. | MERID-003 (IN PROGRESS) |
| OCM / Prosci | 🟢 **GREEN** | Sub-vendor kick-off complete. Stakeholder mapping in progress. On track for Phase 0 exit deliverable. | MERID-007 (DONE) |

**Phase 0 gate: 2026-10-06 — 5 days.** Gate will not pass while SAP credentials are outstanding (Phase 1 entry criterion: "SAP credentials provisioned to EPAM dev environment"). Gate may pass with disputed codes pending only if the arbiter ruling arrives by 2026-10-02 and the final root-cause % ≥ 40%.

---

## Top 3 Active Risks

**Risk #2 — SAP ECC access delayed** (Risk Register row 2 | L:3 × I:4 = High | Expected cost: €4,500)
Day 7, no credentials, no Meridian IT timeline. Active mitigation: EPAM right-to-pause clock running per Assumption A1 (right-to-pause starts Day 6; each day of delay shifts Phase 1 start day-for-day at no cost to Meridian). SA and DE1 redeployment to available work is the cost buffer. **Next contractual trigger:** if credentials not received by Day 10 (2026-10-04), either party may initiate termination notice for Phase 1+ per Assumption A1.

**Risk #3 — POS data quality <80% in both candidate countries** (Risk Register row 3 | L:3 × I:3 = High | Expected cost: €2,700)
France is currently at 71% and unlikely to meet the gate. Germany at 84.2% meets the gate. Active mitigation: Phase 0 exit criterion allows restriction to one country — pilot proceeds Germany-only. Cost: no additional scope change cost; statistical power of measurement reduced (single country). Programme Director sign-off on Germany-only scope is required at Phase 0 gate.

**Risk #1 — Root-cause gate uncertainty** (Risk Register row 1 | L:3 × I:5 = High | Expected cost: €9,900)
2 codes remain disputed. If both disputed codes resolve as allocation-driven, the root-cause % increases; if operational, it may approach the 40% threshold boundary. Arbiter ruling due 2026-10-02 is binding with no further dispute mechanism. Current status: 14/16 classified, 2 disputed — cannot confirm final % until ruling.

---

## Top 3 Decisions Needed This Week

| # | Decision | Decision owner | Deadline | Stakes |
|---|----------|---------------|----------|--------|
| D1 | **Invoke right-to-pause formally?** SAP credentials are Day 7 overdue. Should EPAM EL issue the formal right-to-pause notice to Meridian now, or wait until Day 10 before the termination window opens? Waiting until Day 10 loses 3 days of documented trail if Phase 1 is delayed. | EPAM Engagement Lead | 2026-10-02 | Phase 1 start date; contractual paper trail |
| D2 | **Germany-only scope — Programme Director acknowledgement.** France is at 71% and will not meet the gate. Does Meridian Programme Director formally accept Germany-only pilot scope at the Phase 0 gate, or does the engagement pause pending France data remediation? | Meridian Programme Director | 2026-10-06 (Phase 0 gate) | Phase 1 scope; measurement report statistical power |
| D3 | **Phase 0 gate timing if SAP credentials arrive late.** If credentials arrive 2026-10-03 or 2026-10-04, the Phase 0 gate on 2026-10-06 would provide only 1–2 days to confirm environment setup. Should Phase 0 gate be extended to 2026-10-08 (adding 2 days), or does the gate proceed with provisioning deferred to Phase 1 week 1? | EPAM Engagement Lead + Meridian Programme Director | 2026-10-04 | Phase 1 start date; SAP buffer contingency |

*These decisions are named for steering-committee input. EPAM Engagement Lead does not commit dates or scope without Meridian Programme Director sign-off.*
