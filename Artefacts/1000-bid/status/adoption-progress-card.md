---
engagement: Meridian UC1.1 Pilot
week: Phase 0 Week 2
card_date: 2026-10-01
source: 06-ai-native.md
---

# AI-Adoption Progress Card — 2026-10-01

*Per SDLC phase: current L0–L3 level vs. target from 06-ai-native.md, evidence from sprint signal, biggest gap.*

| SDLC Phase | Engagement Phase | Target | Current | Evidence | Biggest Gap |
|-----------|-----------------|--------|---------|----------|-------------|
| **Intake** | Phase 0, weeks 1–2 | L1 by month 1 | **L1 — MET** | 14/16 reason codes (87.5%) have DIAL-assisted draft reviewed before analyst finalisation. DIAL session log confirms 82% of token usage on classification task. Threshold ≥80% by week 2 met. | 2 disputed codes not yet covered — arbiter ruling due 2026-10-02; final classification not DIAL-assisted (human ruling). Disputed codes will remain L0 for those 2 rows until classified. |
| **Plan** | Phase 0/1 boundary, weeks 2–3 | L1 by month 1; L2 by month 2 | **L0 — not yet active** | Sprint planning for Phase 1 has not started. No DIAL-assisted AC drafts produced yet. | Phase 1 sprint backlog must be drafted before Phase 1 start (2026-10-07+). DIAL-assisted AC drafting workflow needs to be set up by EPAM PM in week 3 to hit L1 on schedule. |
| **Build** | Phases 1–2, weeks 3–10 | L2 by month 2; L3 stretch by month 3 | **L0 — not yet active** | No code commits yet; model build starts Phase 1. | Copilot PR tagging workflow (06-ai-native.md: `copilot-assisted` PR label) needs to be configured before first Phase 1 PR is merged. Not yet done — risk of retroactive untagged PRs reducing the adoption metric denominator. |
| **Validate** | Phase 2 exit + Phase 3 | L2 by month 3 | **L0 — not yet active** | Not applicable until Phase 2 sprint 3+ (≥ week 8). | Dashboard test plan YAML structure (with `ai-generated: true` flag per test case) should be templated in Phase 1 before any test generation begins, so the denominator is correct from the first test. |
| **Handoff** | Phase 3, weeks 11–12 | L2 by month 3 | **L0 — not yet active** | Not applicable until Phase 3. | Handover checklist template with `ai-draft: true` section metadata should be created in Phase 2 — the template is easier to populate with metadata during build than retrospectively at handover. |
| **Learn** | Phase 3 + retros throughout | L1 by pilot close | **L0 → approaching L1** | DIAL retro note synthesis: 6% of week 2 token usage. Retro output (2026-10-01) was partially synthesised using DIAL. Not yet systematic — not measured against a denominator. | Target metric (06-ai-native.md: ≥60% of retro action items with DIAL-assisted synthesis by retro 3) requires the EPAM PM to tag action items by source. Tagging workflow not yet in place. Start in Phase 1 retro 1 (week 4). |

## Summary

- **1 of 6 phases** at target (Intake = L1 ✅).
- **5 of 6 phases** at L0 — appropriate for Phase 0 week 2; Build, Validate, Handoff are not yet active.
- **Proactive gaps to close before Phase 1 starts:** (a) DIAL-assisted AC drafting workflow for Plan phase; (b) Copilot PR label configuration for Build phase; (c) retro action-item tagging for Learn phase.
- No combination warning: Intake L1 is supported by DIAL token evidence; not a self-reported claim.
