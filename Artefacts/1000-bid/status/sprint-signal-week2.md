---
engagement: Meridian UC1.1 Pilot
week: 2 (Phase 0 — Discovery & Gate)
signal_date: 2026-10-01
---

# Sprint Signal — Phase 0 Week 2

## Jira Export

| Ticket | Summary | Status | Assignee | Notes |
|--------|---------|--------|----------|-------|
| MERID-001 | Root-cause diagnostic: POS reason-code classification | IN PROGRESS | DE1 | 14/16 reason codes classified using DIAL-assisted drafts; 2 codes disputed (see MERID-006) |
| MERID-002 | POS completeness audit — Germany | DONE | DE1 | Result: 84.2% completeness (≥80% gate met for Germany) |
| MERID-003 | POS completeness audit — France | IN PROGRESS | DE2 | Preliminary: 71% completeness; France gate likely to fail |
| MERID-004 | SAP ECC read-only credential request | BLOCKED | EL | SAP credentials NOT received. Day 7 (Day 5 deadline was 2026-09-29). Meridian IT acknowledged the request; no timeline given. |
| MERID-005 | EPAM dev environment — EU-region provisioning | DONE | DE1 | Complete; EU-region data classification CLIENT_CONFIDENTIAL applied |
| MERID-006 | Disputed reason-code arbitration | OPEN | EL | 2 codes disputed: (1) "inter-store transfer lag" — Meridian Data team classifies as store-execution; EPAM classifies as allocation-driven. (2) "order cancellation — supplier OOS" — classification unclear. Escalated to Meridian Head of Retail Planning per methodology. Ruling due 2026-10-02. |
| MERID-007 | Prosci sub-vendor kick-off | DONE | PM | Prosci engagement confirmed; stakeholder mapping started |
| MERID-008 | Phase 0 kick-off meeting | DONE | EL | Executive Sponsor (CSCO) attended; all parties aligned on methodology |

**Sprint velocity:** 5 story points delivered / 8 planned (62.5%). Blocked: MERID-003 (France) waiting on additional POS export from Meridian IT; MERID-004 (SAP) blocked on Meridian IT.

---

## AI-Gateway Log (EPAM DIAL + GitHub Copilot)

| Tool | Metric | Week 2 value | Week 1 value | Delta |
|------|--------|-------------|-------------|-------|
| EPAM DIAL | Input tokens | 520,000 | 310,000 | +68% |
| EPAM DIAL | Output tokens | 13,500 | 8,200 | +65% |
| EPAM DIAL | Estimated cost (EU endpoint) | €1.62 | €0.96 | +69% |
| GitHub Copilot | Active users | 4 | 3 | +1 |
| GitHub Copilot | Completions accepted | 312 | 198 | +57% |
| GitHub Copilot | Completions shown | 398 | 267 | +49% |
| GitHub Copilot | Acceptance rate | 78.4% | 74.2% | +4.2pp |

DIAL usage breakdown: reason-code classification drafts (82% of tokens), Python POS parsing scripts (12%), retro note synthesis (6%).

Weekly DIAL cost €1.62 is within the M800 budget ceiling (€130/month AI tooling allocation for pilot phase = €32.50/week; current run rate is well below ceiling).

---

## Retro Output (Phase 0 Sprint 1 + 2 combined retro — 2026-10-01)

**What worked:**
- DIAL reason-code classification workflow saved ~60% of manual classification time; 14/16 codes agreed on first pass
- Germany POS audit completed ahead of schedule; 84.2% confirms the pilot can proceed in Germany
- Prosci kick-off smooth; stakeholder mapping started in Phase 0 as planned

**What didn't:**
- SAP credentials not received by Day 5 — right-to-pause clock is running (Day 7 today). Meridian IT has not provided a timeline. This is the highest-risk item going into the Phase 0 gate on 2026-10-06.
- France POS completeness (71%) is below the 80% gate — France will likely be excluded from pilot scope. Germany only.
- 2 disputed reason codes not yet resolved; Head of Retail Planning ruling due 2026-10-02 but not confirmed.

**Actions from retro:**
- EL to escalate SAP credentials to Meridian IT Director by COB 2026-10-02 if no timeline is provided by Meridian IT lead
- EL to confirm with Meridian Programme Director that France exclusion is understood and accepted
- PM to confirm Prosci stakeholder mapping deliverable date (Phase 0 exit criterion)
