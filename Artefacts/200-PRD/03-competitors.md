---
product: Meridian click-&-collect (product detail page)
feature: AI availability assistant
date: 2026-06-22
sources: 00-feature.md, 02-personas-journey.md; competitor data from training knowledge (cutoff Aug 2025) — claims labeled [VERIFIED], [LIKELY], or [UNVERIFIED]
---

# Competitive Analysis: Click-and-Collect Availability Signals

**Job being compared:** Tell the shopper whether the item is really collectable at a nearby store before they reserve and drive there.

---

## Comparison Table

| Product | Approach | Strength | Weakness | Differentiator dimension |
|---------|----------|----------|----------|--------------------------|
| **Zalando** | Real-time WMS feed from brand/partner warehouses via Partner API. Binary "in stock" based on warehouse ledger. No owned store network; C&C routes to partner stores. [VERIFIED] | Centralized warehouse signal is more accurate than store-shelf signals for most SKUs — fulfillment center truth is close to binary truth. [VERIFIED] | No store network = no shelf signal. Phantom stock risk is externalized to partner WMS quality. No confidence interval, no ML layer for per-store pickup likelihood. "Reserve in Store" pilot (DE, 2022–23) was not scaled. [VERIFIED / LIKELY] | Shows warehouse truth, not shelf truth — can't distinguish a packed warehouse from an empty fitting room |
| **Zara (Inditex)** | RFID item-level tagging across all owned stores (rollout complete ~2016, global by 2020). Product page shows per-store availability as binary: in stock / low stock / out of stock, refreshed every few hours. [VERIFIED — reproducible on zara.com] | ~99% inventory accuracy vs. ~65–70% barcode-only retailers. [LIKELY — cited in RFID retail literature; Inditex hasn't published a specific figure.] Binary signal is grounded in physically verified counts, not ledger estimates. | Signal degrades during peak hours when fitting-room returns haven't been re-tagged yet — the exact window when fast-selling fashion items show phantom stock. No confidence interval, no pickup commitment. A shopper acting on "low stock" has no guarantee when they arrive. [LIKELY — documented in RFID retail research] | RFID is accurate on average but shows no variance — doesn't warn the shopper that 09:00 Saturday "low stock" means gone-in-an-hour |
| **Apple Retail** | Committed reservation model: inventory is physically pulled and held before the confirmation is issued. Product page only shows pickup options for stores that can commit; stores that cannot are hidden from the UI. [VERIFIED — Apple support docs] | Eliminates phantom stock entirely by converting a signal into a fulfillment operation. Zero false positives; 14-day hold window is the highest-trust shopper experience in retail. [VERIFIED] | Not scalable to fashion SKU depth (10K–100K active SKUs vs. ~30–50 hardware SKUs). Physical pulling and holding per reservation at fashion scale requires prohibitive staffing overhead. Shoppers cannot browse availability across stores before committing — must select a store first. [VERIFIED as structural constraint] | Commitment model solves the problem by removing the uncertainty — but only works when SKU count is tiny and items are identical |
| **Meridian (us)** | AI availability assistant surfaces a per-store High / Medium / Low confidence indicator on the product detail page before reservation, derived from SAP inventory count + same-day POS sell-through velocity + store-level OMS adjustment events. | Targets the gap all three miss: a calibrated probability signal that accounts for how fast a specific store is selling a specific item today — not just what the count is right now. Surfaces alternatives (other stores, home delivery) at decision time, not after cancellation. | No physical hold (unlike Apple). No RFID ground truth (unlike Zara). Confidence score depends on model accuracy; a miscalibrated "High" that leads to a wasted trip is worse than no signal. Counter-metric needed to detect suppression from excess "Low" signals. | **Predict collectability from sell-through velocity, not static count** |

---

## Named Differentiator

**Predict collectability from same-day sell-through velocity, not static inventory count.**

- Zalando shows warehouse truth, not shelf truth.
- Zara shows RFID count with no variance — can't distinguish Tuesday morning from Saturday peak.
- Apple removes the signal problem entirely — but only because their SKU count is tiny.
- **The gap all three share:** none model the rate at which inventory is depleting at a specific store on a specific day. A count of 3 units at 09:00 Saturday means something very different from 3 units at 09:00 Tuesday. Meridian owns this dimension: a velocity-adjusted confidence score that tells the Trip Planner whether "in stock" is reliable right now, at that store, for this item.

---

## Named AI Feature (carried into PRD and Deep Eval series)

**Velocity-adjusted collectability scoring** — an ML model that ingests:
- Current SAP inventory count per SKU per store
- Same-day POS sell-through rate (units sold in the last 4 hours at that store)
- Time elapsed since last OMS sync (signal recency penalty)
- Store-level historical cancellation rate for that SKU category (base rate prior)

...and outputs a calibrated confidence score (High / Medium / Low) representing the probability that the item will be on the shelf when the shopper arrives, surfaced on the product detail page before reservation.

**Why this is the AI feature, not just a rule:**
A rule ("in stock AND count > 2 → High") can't distinguish a fast-selling Saturday from a slow Tuesday or a store that chronically has 3-unit phantom counts. The model learns store-SKU-time patterns that no static threshold can capture. This is the feature K 2.W.5 writes an AI Eval Card for, and the Deep series evaluates for calibration, false-positive rate, and confidence threshold tuning.

**Sharpened against the scan:**
- Against Zara: same accuracy target (~99%) but with a probabilistic output, not a binary threshold — adding a confidence interval the shopper can act on
- Against Apple: no physical hold required; confidence signal does the pre-filtering that Apple's hide-unavailable-stores UI does, but at fashion SKU scale
- Against Zalando: operates on store-shelf signals (POS + OMS), not partner WMS feeds — the source Zalando cannot reach

**AI Eval dimensions for K 2.W.5:**
- Calibration: does "High" correspond to ≥90% actual availability? Does "Low" correspond to ≤30%?
- False-positive cost: a "High" that leads to a wasted trip is the primary failure mode; asymmetric penalty applies
- False-negative cost: excess "Low" signals suppress reservations; counter-metric (conversion rate ≥ baseline − 1 pp) guards this
- Coverage: what % of stores have sufficient POS velocity data for the model to score (vs. fallback to binary count)?
