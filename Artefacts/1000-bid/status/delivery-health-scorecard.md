---
engagement: Meridian UC1.1 Pilot
week: Phase 0 Week 2
scorecard_date: 2026-10-01
---

# Delivery Health Scorecard — 2026-10-01

## DORA Indicators

*Note: Phase 0 is an analysis and diagnostic phase — no production code is deployed. DORA metrics that require production deployment (deployment frequency, change-failure rate, time-to-restore) are not applicable until Phase 2 dashboard deployment. Lead time is tracked as analysis task cycle time.*

| Indicator | Value | Status | Notes |
|-----------|-------|--------|-------|
| Deployment frequency | N/A (Phase 0) | — | No production deployments in Phase 0. First deployment: dashboard to EPAM EU dev environment in Phase 2 week 1 (~2026-10-28). |
| Lead time (task cycle time proxy) | 2.5 days avg | 🟢 GREEN | Completed tickets: MERID-002 (POS audit), MERID-005 (dev env), MERID-007 (Prosci kick-off), MERID-008 (kick-off meeting). 4 tickets completed in 10 days = 2.5 days avg cycle time. |
| Change-failure rate | N/A (Phase 0) | — | Not applicable until Phase 2. |
| Time-to-restore | N/A (Phase 0) | — | Not applicable until Phase 2. |
| Sprint velocity | 62.5% (5/8 SP) | 🟡 AMBER | Below target; 2 blocked tickets (MERID-004 SAP, MERID-003 France) are client-dependency blockers, not EPAM delivery failures. Velocity on EPAM-owned tasks: 5/6 = 83%. |

## AI Adoption Rate

*Source: 06-ai-native.md Intake phase target: ≥80% of reason codes with DIAL-assisted draft by week 2.*

| Metric | Value | Target | Status | Denominator |
|--------|-------|--------|--------|-------------|
| Reason codes with DIAL-assisted draft | 14/16 = **87.5%** | ≥80% by week 2 | 🟢 GREEN — **L1 target met** | 16 total distinct reason codes in 12-month POS dataset |
| Copilot acceptance rate | 78.4% | No week-2 target set (baseline measurement) | 🟢 GREEN baseline | 398 completions shown |
| Copilot active users | 4/7 team members | No week-2 target set | Tracking only | 7 in Balanced team; 4 roles active in Phase 0 |

## DIAL Cost Attribution

*Source: AI-gateway log. M800 budget ceiling: €130/month = €32.50/week.*

| Tool | Week 2 cost | Week 1 cost | Delta | vs. Weekly ceiling |
|------|------------|------------|-------|-------------------|
| EPAM DIAL | €1.62 | €0.96 | +69% | €1.62 / €32.50 = **5% of ceiling** |
| GitHub Copilot | Covered by EPAM pre-approved licence (no per-usage cost) | — | — | Within pre-approved allocation |
| **Total AI tooling** | **€1.62** | **€0.96** | +69% | **5% of weekly ceiling — well within budget** |

## Combination Read

| Combination | Values | Signal |
|-------------|--------|--------|
| DIAL tokens ↑ (+68%) + Copilot acceptance rate ↑ (+4.2pp) | Both positive | 🟢 **No combination warning** — usage growth matches quality signal. DIAL token increase is driven by more reason codes being processed (week 2 = active classification phase). |
| Velocity AMBER + SAP blocked | Velocity drop is client-dependency driven | 🟡 **Attribution note** — velocity metric understates team productivity; blocked tickets have client-side owners. EPAM-owned task velocity is 83%. |
| DIAL cost ↑ (+69%) + within ceiling | Cost increase is proportional to work volume | 🟢 **No cost warning** — €1.62 is 5% of weekly ceiling; trajectory of current phase stays under ceiling even at 3× this rate. |
