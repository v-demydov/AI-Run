---
product: Meridian click-&-collect (product detail page)
feature: AI availability assistant
date: 2026-06-22
sources: 01-vision.md (metrics) · 04-stories-acs.md · 05-backlog.csv
---

# Traceability Matrix

**Outcome metrics (from 01-vision.md v2):**
- **M1** — C&C cancellation-at-pickup rate: 7% → ≤4% within 90 days (primary)
- **M2** — C&C reservation conversion rate: ≥ baseline − 1 pp (protective guardrail)

---

## Story → Metric Links

| Story | How it moves M1 | How it moves M2 | Sprint | Status |
|-------|----------------|----------------|--------|--------|
| **S1** Confidence indicator | ✅ Direct: reduces High false positives; shoppers with accurate signal make better decisions → fewer wasted trips → lower cancellation rate | ⚠️ Watch: shoppers seeing Medium/Low may not reserve; conversion could dip. Counter-metric exists to detect this. | 1 | Included |
| **S7** Fallback safety | ✅ Direct: prevents degraded-state from generating false-High confidence → eliminates phantom-stock failures during model outage | — | 1 | Included |
| **S4** Warning modal | ✅ Direct: intercepts Low-confidence reservations before the shopper commits to the trip; a shopper who heeds the warning does not become a M1 cancellation | ⚠️ Watch: some shoppers abandon at warning rather than choosing an alternative; M2 counter-metric guards this | 1 | Included |
| **S3** Velocity signal | ✅ Direct: improves model precision on High during peak-velocity periods (flash sales, weekends); fewer flash-sale false positives → M1 improvement | — | 1 | Included |
| **S9** Accessibility | — No direct metric link | — | 1 | ⚠️ No metric link — WCAG 2.1 AA compliance requirement; treat as quality attribute of S4, not a story driving M1/M2 |
| **S2** Alternative stores | ✅ Direct: converts Low-confidence sessions that would otherwise cancel into successful pickups at higher-confidence stores | ✅ Direct: retains conversions that would abandon on seeing Low with no alternative | Post-S1 | Deferred — blocked by S1 calibration data |
| **S6** Timestamp | ⚠️ Marginal: a shopper who sees a stale signal and decides not to reserve avoids a potential M1 cancellation; effect size too small to measure | — | Post-S1 | Deferred |
| **S11** Logging | — No direct metric link | — | Post-S1 | ⚠️ No metric link — M1 measurement dependency: without confidence logs, we cannot measure model calibration (High-correctness %) needed to track whether M1 improvement is attributable to signal accuracy. Required technical enabler, not a metric driver. |
| **S10** Ops monitoring | — No direct metric link | — | Icebox | ⚠️ No metric link — indirect: if ops teams investigate and fix root-cause phantom-stock stores, M1 may improve. But the link is too indirect and too slow to count. Schedule only after 90 days of S1 data. |

---

## Flags

### Stories with no metric link

| Story | Type | Disposition |
|-------|------|-------------|
| S9 — Accessibility | Legal compliance / quality attribute | Keep — required for WCAG 2.1 AA and EU consumer protection; bake into S4 delivery cost, do not treat as standalone story driving metrics |
| S11 — Logging | Technical enabler | Keep — required to measure M1 calibration (without it, we can't confirm the circuit breaker threshold); schedule alongside S6 post-S1 launch |
| S10 — Ops monitoring | Indirect / too slow | Icebox — link to M1 is real but too indirect and too slow (90+ days lag) to justify in backlog; review post-S1 data |

### Dead metrics check

| Metric | Stories driving it | Status |
|--------|-------------------|--------|
| M1 — Cancellation rate | S1, S7, S4, S3, S2 (deferred) | ✅ Not dead — 4 Sprint 1 stories directly drive it |
| M2 — Conversion rate | S1 (watch), S4 (watch), S2 (direct, deferred) | ⚠️ Guardrail only — no Sprint 1 story is designed to *improve* M2; all links are protective. This is correct: M2 is a counter-metric, not a growth target. If M2 drops by >1 pp, the signal is too aggressive and needs recalibration — that's the design intent. |

### M2 interpretation note
M2 has no story that drives it upward — only stories that could hurt it (S1, S4) and one that protects it (S2, deferred). This is by design: the feature's goal is to inform shoppers accurately, which may reduce conversion for items that genuinely have low availability. A drop in M2 that is accompanied by a drop in M1 is an acceptable outcome. A drop in M2 without a corresponding drop in M1 (excess Low signals suppressing demand for items that were actually available) is the failure mode the counter-metric exists to catch.
