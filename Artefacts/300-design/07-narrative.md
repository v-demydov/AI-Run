---
product: Meridian click-&-collect (product detail page)
date: 2026-06-24
sources: 06-prd.md · 05-backlog.csv · 03-decision.md · 07-validation-plan.md
audience: Sarah Chen (Head of CX) · steering committee · sprint kick-off
---

# Redesign Narrative: Availability Confidence Feature

---

## The problem in one number

**7%** of Meridian click-and-collect orders end in cancellation at the pickup counter.
The shopper has already made the trip. The binary "In stock" label they trusted was technically accurate — it reflected the ERP count at the last sync — and practically wrong, because same-day sales between syncs had cleared the shelf.

After one failure, the majority of affected shoppers defect to Zalando or ASOS.
The feature does not leak at conversion. It leaks after the trip.

---

## The change

Replace the binary "In stock" label with a **three-state confidence indicator** (High / Medium / Low), derived from same-day POS sell-through velocity and SAP inventory count. Add a **friction modal** that intercepts the Reserve tap when the nearest store shows Low confidence, with "Choose another store" as the default action.

The feature does not remove the shopper's ability to reserve. It moves the risk disclosure to before the trip rather than at the counter.

---

## Benefit

The primary gain is **prevented wasted trips** — for the shopper (time, travel cost) and for Meridian (cancellation handling, trust repair, competitor defection).

Secondary gains:
- Shoppers who redirect to a High-confidence store are successful pickups, not cancellations.
- The logged confidence signal enables ongoing model calibration — each pickup outcome is a data point that improves the next prediction.
- A High label with a visible staleness timestamp is a truthful disclosure; Meridian's legal exposure from misleading availability claims is reduced.

---

## Engineering cost

| Work item | Effort | Condition |
|-----------|--------|-----------|
| S1 — Confidence scoring model + API + product page integration | 13 pw | Unconditional |
| S7 — Fallback safety (cached OMS snapshot, staleness notice) | 3 pw | Ships with S1 |
| S4 — Low-confidence friction modal (WCAG 2.1 AA) | 3 pw | Ships with S1 |
| S3 — Same-day POS velocity signal in model | 6 pw | Conditional on 4-week offline calibration experiment passing (≥5% MAPE improvement) |
| S9 — Screen-reader accessibility | 1 pw | Baked into S4 |

**Sprint 1 total:** 20–26 person-weeks depending on S3 result.
S3 offline experiment runs in parallel before sprint kick-off; S1 ships with SAP-only model if experiment fails; S3 added in Sprint 2.

---

## Design cost

| Work item | Effort |
|-----------|--------|
| ConfidenceBadge + StalenessBadge component design + tokens | 1 pw |
| FrictionModal design + accessibility review | 0.5 pw |
| Copy sign-off (4 label strings + modal + staleness variants) | 0.5 pw |
| Handoff pack (CONTEXT.md + SPEC.md + prototype) | Already complete |

**Design total:** ~2 person-weeks. Spec and prototype are complete; remaining cost is token integration with the project design system and copy sign-off.

---

## Content cost

4 label strings require brand/legal sign-off:
- "Likely available" (High)
- "May vary — check before travelling" (Medium)
- "May not be available" (Low)
- "Availability unknown" (Fallback)

Plus the modal body: "Our system suggests this item may not be on the shelf at [store] when you arrive."

**Content total:** 0.5 person-weeks. The constraint is legal review of "not a committed hold" disclosure language, not writing effort.

---

## The one number

> **C&C cancellation-at-pickup rate: 7% → ≤ 4% within 90 days of launch.**

This is a 43% reduction in cancellations, measured weekly from OMS data, code "item unavailable at pickup."

**How the feature gets there:**
- Shoppers who see High confidence and travel have a ≥ 85% pickup success rate (model calibration target).
- Shoppers who see Low confidence and redirect to a better store or do not travel do not become cancellations.
- Shoppers in the friction modal who tap "Reserve anyway" at a Low store are informed consent; their cancellation rate is expected to remain high, but they are a minority of all reservations.

**Counter-metric (M2):** C&C reservation conversion rate must not drop by more than 1 percentage point. A drop greater than 1 pp signals the confidence signal is suppressing demand for items that were actually available — requiring recalibration, not feature removal.

**Measurement gate:** M1 and M2 are reviewed weekly for 90 days post-launch. At 90 days, the team decides whether to open the evidence gate for S2 (alternative stores) or recalibrate the model.

---

## What failure looks like

The feature fails in two ways, not one:

**Failure mode A — model miscalibration:** High-correctness falls below 75%; circuit breaker fires; the feature auto-reverts to binary fallback. The cancellation rate stays at 7%. Action: root-cause the model, fix, re-enable manually.

**Failure mode B — signal suppression:** M1 improves but M2 drops by >1 pp. The confidence signal is correctly identifying low-availability stores but is also suppressing legitimate reservations at Medium-confidence stores where the item was genuinely available. Action: widen the High threshold or add "choose a different store" default only for Low (not Medium).

Neither failure mode is silent. Both are caught by the weekly metric review before 90 days.
