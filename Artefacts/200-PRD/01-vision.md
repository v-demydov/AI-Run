---
product: Meridian click-&-collect (product detail page)
feature: AI availability assistant
date: 2026-06-22
status: draft v2 — post-adversarial review
---

## Vision (draft v1)

Meridian click-&-collect shoppers will step into stores knowing their reserved item is actually on the shelf. Today, one in fourteen click-&-collect orders ends in a cancellation at pickup — not because the item sold out after reservation, but because the system never knew shelf reality in the first place. The AI availability assistant surfaces a per-store confidence signal (High / Medium / Low) on the product detail page before the shopper commits to a reservation, converting a hidden infrastructure failure into a visible, shopper-owned decision. When shoppers can trust the channel, fewer trips are wasted, fewer orders cancelled, and fewer customers defect to Zalando.

## Problem Statement

7% of Meridian click-&-collect orders are cancelled at pickup because online inventory counts fail to reflect real shelf availability, eroding shopper trust and driving defection to competitors.

## Target User

Click-&-collect shoppers who reserve online specifically to avoid a wasted trip to store — behaviorally: shoppers choosing click-&-collect over home delivery, or shoppers with ≥1 prior cancelled pickup.

## Outcome Metric

Click-&-collect cancellation-at-pickup rate decreases from 7% to ≤4% within 90 days of full launch, measured weekly against Meridian order management system cancellation codes (filter: "item unavailable at pickup").

---

## Adversarial Critiques (fresh session)

**Critique 1 — The confidence signal is a UI patch on a data infrastructure problem the PM hasn't proven exists.**
The vision asserts a "per-store confidence signal" without naming the model inputs. If the system "never knew shelf reality," where does the signal come from? If POS velocity, adjustment events, or shrinkage data aren't already captured at per-store granularity, there's no ground truth — just a reassuring label on noise. Fix: name the specific data sources and their current coverage before any product work begins.

**Critique 2 — The outcome metric is trivially gameable and doesn't prove the feature worked.**
Cancellation rate drops to zero if the signal defaults to "Low" often enough to suppress reservations, or if shoppers abandon the channel entirely after too many Low signals. Engineering could ship a feature that devastates top-of-funnel and the PM declares victory. Fix: add a paired counter-metric — click-&-collect reservation conversion rate must hold flat or improve.

**Critique 3 — The causal claim that cancellations drive Zalando defection is asserted, not evidenced, and it changes the entire investment thesis.**
There is no data connecting cancelled pickups to competitor switching. If defection is real and quantifiable, this is a retention problem worth significant investment. If it's not, the ROI case collapses to a marginal UX fix for a niche channel. Fix: cite post-cancellation cohort behavior from Meridian CRM (repurchase rate, channel shift, 90-day revenue), or drop the Zalando claim and size the problem on cancellation volume alone.

---

## Vision (revised v2)

Meridian click-&-collect shoppers will complete pickups at the rate they reserve — eliminating the one-in-fourteen cancellation that signals a broken channel. The AI availability assistant synthesises per-store SAP inventory counts, same-day POS velocity, and store-level adjustment events (all already flowing through Meridian's OMS) to generate a confidence indicator on the product detail page before reservation. A shopper who sees "Low confidence" can choose a different store or shift to home delivery instead of driving over to an empty shelf — turning a silent data-quality failure into a visible, shopper-controlled decision.

**Problem statement (v2):** 7% of Meridian click-&-collect orders are cancelled at pickup because SAP inventory counts don't reflect same-day POS deductions and in-store adjustments; the reliability gap is measurable, the input data is already captured, and it suppresses repeat channel usage.

**Target user (v2):** Click-&-collect shoppers reserving online to avoid a wasted trip — specifically those in stores where same-day POS velocity is high enough to create phantom stock (quantified at pilot-scoping stage from OMS data).

**Outcome metrics (v2):**
- Primary: click-&-collect cancellation-at-pickup rate falls from 7% to ≤4% within 90 days of full launch (OMS cancellation code "item unavailable at pickup", measured weekly)
- Counter-metric: click-&-collect reservation conversion rate holds at ≥ baseline − 1 pp (guards against channel suppression from excess Low-confidence signals)
