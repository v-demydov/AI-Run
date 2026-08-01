---
engagement: Meridian UC1.1 Pilot
week: Phase 0 Week 2
actions_date: 2026-10-01
tripped_indicators: 3
---

# Go-to-Green Actions — 2026-10-01

*One named action per tripped indicator. Owner is the role from 05-plan.md. Target date from milestone table. Gate unlocked stated.*

---

## Action 1 — SAP Credentials (🔴 RED)

| Field | Value |
|-------|-------|
| **Indicator** | SAP ECC credentials not received — Day 7 of 5-day window (right-to-pause clock running per Assumption A1) |
| **Action** | EPAM EL to issue written escalation to Meridian IT Director (cc: Meridian Programme Director) by COB 2026-10-02 requesting a confirmed credential delivery date. If no timeline received by Day 10 (2026-10-04), EPAM EL to invoke formal right-to-pause notice per Assumption A1 and notify EPAM Delivery Director. |
| **Owner** | EPAM Engagement Lead |
| **Target date** | Escalation email: **2026-10-02 COB**; right-to-pause notice if needed: **2026-10-04** |
| **Gate unlocked** | Phase 1 entry criterion: "SAP ECC read-only credentials provisioned to EPAM dev environment" (05-plan.md M3) |
| **Decision boundary** | Whether to issue the formal right-to-pause notice is a human-owned call — EPAM EL decides, not this agent. This action escalates; it does not commit. |

---

## Action 2 — Disputed Reason Codes (🟡 AMBER)

| Field | Value |
|-------|-------|
| **Indicator** | 2 reason codes disputed; Phase 0 root-cause % cannot be confirmed until arbiter ruling |
| **Action** | EPAM EL to confirm with Meridian Programme Director that the Head of Retail Planning ruling is scheduled for 2026-10-02. If not confirmed by 2026-10-02 09:00, EPAM EL to request a same-day written ruling (per Phase 0 methodology: binding ruling within 2 business days; non-re-openable after). PM to update MERID-006 in Jira with ruling outcome as soon as received. |
| **Owner** | EPAM Engagement Lead (confirmation) · EPAM PM (Jira update) |
| **Target date** | Ruling confirmation: **2026-10-02 09:00**; Jira update: **2026-10-02 EOD** |
| **Gate unlocked** | Phase 0 exit criterion: root-cause ≥40% confirmed (05-plan.md M2); confirmed root-cause % is required for Phase 0 gate on 2026-10-06 |
| **Note** | If both disputed codes resolve as operational (not allocation-driven), the final root-cause % may approach or fall below 40%. EPAM EL must be briefed on the ruling before the Phase 0 gate meeting — not during it. |

---

## Action 3 — France Pilot Scope (🟡 AMBER)

| Field | Value |
|-------|-------|
| **Indicator** | France POS completeness 71% — below the 80% gate; pilot will be Germany-only; Meridian Programme Director has not formally acknowledged scope restriction |
| **Action** | EPAM PM to prepare a 1-paragraph scope-change note (Germany-only pilot, France excluded per Phase 0 POS gate criterion) for EPAM EL to send to Meridian Programme Director for written acknowledgement before Phase 0 gate meeting on 2026-10-06. This is an expected outcome per Assumption A3 in 04-estimate.xlsx — no commercial change order is required; scope restriction is within the existing SOW terms. |
| **Owner** | EPAM PM (note preparation) · EPAM Engagement Lead (send and obtain written acknowledgement) |
| **Target date** | Note prepared: **2026-10-04**; written acknowledgement from Meridian Programme Director: **2026-10-06 (Phase 0 gate meeting)** |
| **Gate unlocked** | Phase 0 exit criterion: "POS completeness ≥80% in ≥1 pilot country" — Germany at 84.2% meets the gate; Programme Director acknowledgement of Germany-only scope is required for the gate to close cleanly (05-plan.md M2) |

---

## Proactive Actions — Not Yet RED/AMBER, but Gap to Close Before Phase 1

| Action | Owner | Target | Why now |
|--------|-------|--------|---------|
| Configure Copilot PR label (`copilot-assisted`) in GitHub repository before first Phase 1 PR is merged | EPAM Data Engineer 1 | 2026-10-07 (Phase 1 day 1) | Without the label, the Build adoption metric denominator is untracked from the start; retroactive tagging is unreliable |
| Set up DIAL-assisted AC drafting workflow for Phase 1 sprint backlog creation | EPAM PM | 2026-10-07 (Phase 1 day 1) | Plan phase L2 target (≥75% of stories with AI-assisted draft AC by sprint 3) requires the workflow to be running from sprint 1 |
| Add retro action-item tagging (DIAL-synthesised: yes/no) to retro template | EPAM PM | 2026-10-10 (Phase 1 retro 1) | Learn phase metric requires a denominator — tagging must start at the first retro where DIAL synthesis is used, not retrospectively |
