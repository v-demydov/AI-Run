---
product: Meridian click-&-collect (product detail page)
feature: AI availability assistant
date: 2026-06-22
status: v1 — ready for engineering review
sources: 01-vision.md · 04-stories-acs.md · 05-backlog.csv
---

# PRD: AI Availability Assistant — Meridian Click & Collect

---

## Problem
7% of Meridian click-&-collect orders are cancelled at pickup because SAP inventory counts do not reflect same-day POS deductions and in-store adjustments. Shoppers drive to store for nothing; after one failure, the majority defect to Zalando or ASOS, which have solved this.

## Vision
Meridian click-&-collect shoppers complete pickups at the rate they reserve — by seeing a velocity-adjusted confidence signal on the product page before they commit to the trip, turning a silent data-quality failure into a visible, shopper-controlled decision.

## Target User
Click-&-collect shoppers reserving online to avoid a wasted trip, at stores where same-day POS velocity is high enough to create phantom stock (quantified from OMS data at pilot scope).

---

## Sprint 1 Delivery Package (S1 · S7 · S4 · S3 · S9)

| Story | Behaviour | Key AC |
|-------|-----------|--------|
| **S1** — Confidence indicator | Product page shows High / Medium / Low before reservation | High = posterior ≥ 0.85 (SAP count + same-day POS velocity + OMS sync age); refusal trigger if count ≤ 0 or SAP sync >4h stale; p95 ≤ 800ms async; circuit breaker if rolling-24h High-correctness < 75% |
| **S7** — Fallback safety | Binary "In stock / Out of stock" when model cannot score | Reads from cached OMS snapshot (not live SAP); if SAP stale >4h: shows staleness warning, not clean positive; p95 ≤ 500ms |
| **S4** — Warning modal | Intercepts reservation tap on Low-confidence store | Focus-trapped dialog (WCAG 2.1 AA); initial focus on "Choose another store"; re-fetches confidence score if >10 min old before evaluating; fail-safe: show modal if re-fetch fails |
| **S3** — Velocity signal | Same-day POS sell-through rate included as model input | Offline experiment on 6 months of POS history must confirm ≥5% MAPE improvement before inclusion; 50% confidence until confirmed |
| **S9** — Accessibility | Screen reader announces confidence label and modal warning | Baked into S4 delivery; `role="dialog"`, `aria-describedby` on warning text; WCAG 2.1 AA |

---

## Scope Boundary

**In scope (Sprint 1):** Velocity-adjusted confidence scoring · fallback safety · Low-confidence warning modal · velocity signal in model · screen-reader accessibility.

**Out of scope (and why):**
- Committed item hold (Apple model) — incompatible with 10K+ fashion SKU depth at 600 stores; requires physical pulls before confirmation
- RFID ground truth (Zara approach) — no Meridian RFID infrastructure; 2–3 year deployment timeline
- Alternative stores (S2) — schedule after 4 weeks of S1 calibration data; Low-confidence trigger rate unknown until S1 is live
- Store map, home delivery fallback, ops monitoring — deferred to post-S1 evidence gate

---

## Success Metrics

| Metric | Baseline | Target | Window | Source |
|--------|----------|--------|--------|--------|
| **M1** C&C cancellation-at-pickup rate | 7% | ≤4% | 90 days post-launch | OMS weekly, code "item unavailable at pickup" |
| **M2** C&C reservation conversion rate | baseline | ≥ baseline − 1 pp | 90 days post-launch | OMS weekly (guard against Low-signal suppression) |

M2 is a protective guardrail, not a growth target. No story is designed to improve it — only to avoid degrading it.

---

## Decision Memory

**Biggest scope call:** Chose a probabilistic confidence signal over a committed item hold.

The committed-hold model (surfaced in the competitor scan from Apple Retail) eliminates phantom stock entirely — no false positives, no wasted trips — and was the obvious solution. It was rejected because the mechanism requires physically pulling and holding items before issuing a confirmation, which is operationally viable only at Apple's SKU depth (~50 hardware SKUs per store). At Meridian's depth (10K–100K active SKUs across 600 stores), the staffing overhead makes the model non-deployable within any defensible budget. The alternative considered and also rejected was an RFID ground-truth initiative (Zara's approach), which achieves ~99% inventory accuracy but requires 2–3 years of infrastructure rollout and tens of millions in hardware investment — solving the same problem, but on a timeline that leaves three more Black Fridays with 7% cancellation rates. The probabilistic ML signal ships in ~13 person-weeks using data Meridian already captures (SAP + POS in OMS), targets a falsifiable outcome (7% → ≤4%), and can be validated in a 12-week pilot before full rollout is approved.
