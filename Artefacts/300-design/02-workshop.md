---
product: Meridian click-&-collect (product detail page)
date: 2026-06-24
sources: 01-journey-map.md · 01-heuristics.md
---

# Workshop Plan + HMW Set: AI Availability Assistant

---

## Part 1 — Workshop Plan

### The one decision to close

> **Do we show estimated availability as a confidence signal on the product page before reservation, or suppress the reservation option for uncertain store–SKU combinations until stock is confirmed?**

These are the only two honest answers to the phantom-stock problem at the product page. A third option — showing no signal and leaving the "In stock" label unchanged — is not on the table: the journey map and heuristic review established that the current label is H1, H5, and H2 violations with High severity at the root of every failure.

**Decision-owner:** Sarah Chen, Head of CX.
Sarah owns the customer experience of the reservation flow. Retail Ops and the regional GM provide constraints; Engineering provides the feasibility ceiling; Sarah closes the call.

---

### Workshop skeleton

| Field | Value |
|-------|-------|
| **Goal** | Decide: confidence signal vs. reservation suppression for uncertain stock |
| **Decision-owner** | Sarah Chen (Head of CX) |
| **Explore** | What form the signal or gate takes; where alternatives are surfaced; what recovery looks like at the counter |
| **Participants** | Sarah Chen (CX) · David Park (Retail Ops) · Marco Rossi (Regional GM) · Engineering lead |
| **Out of scope** | Pricing, loyalty programme, home-delivery fulfilment model, SAP architecture |

---

### Timeboxes

| # | Block | Time | Owner | Output |
|---|-------|------|-------|--------|
| 1 | **Frame** — state the decision, confirm scope, name out-of-scope | 5 min | Sarah Chen | Shared understanding of the one call to make |
| 2 | **Diverge** — HMW questions + silent ideation (post-its or Miro) | 15 min | All | Raw ideas, grouped by HMW, no evaluation |
| 3 | **Converge** — dot-vote on clusters, surface top 3 ideas per theme | 10 min | Sarah Chen (facilitates) | Ranked shortlist to carry into next kata (prototype / decision) |

Total: 30 minutes. If the decision cannot close in 30 minutes, the workshop has surfaced a new ambiguity — capture it and schedule a follow-up with the missing input, not a longer session.

---

### Decision criteria (pre-agreed, used in converge)

| Criterion | Weight | Notes |
|-----------|--------|-------|
| Reduces C&C cancellation at pickup | High | Primary metric M1 from brief |
| Does not suppress reservation conversion by >1 pp | High | Guardrail M2 — any option that gates all uncertainty will fail here |
| Implementable with SAP + OMS data (no new data sources) | Medium | Engineering feasibility ceiling |
| Acceptable to regional GMs (store-level control) | Medium | Marco Rossi input; suppression option likely fails this |
| Shopper understands the signal without instruction | Medium | H2 violation must not be replaced by a different H2 violation |

---

## Part 2 — HMW Questions + Ideas

### How the HMWs were generated

Each HMW names a user moment (a frustration or drop-off from `01-journey-map.md`) — not a feature. HMWs that restated a solution ("how might we build a confidence widget") were rewritten or discarded.

---

### Theme A — Signal before commitment
*How do we put the right signal in front of the shopper before they take on the cost of the trip?*

| # | HMW |
|---|-----|
| A1 | How might we help the shopper understand how reliable today's "in stock" reading is at that specific store — before they tap Reserve? |
| A2 | How might we make the cost of an uncertain reservation visible at the moment the shopper is about to commit to the journey? |
| A3 | How might we prevent the shopper from reserving at a high-risk store without removing their ability to choose? |
| A4 | How might we show the shopper that "in stock" at 9 am and "in stock" at 3 pm on a Saturday mean very different things? |

**Ideas (diverge — no evaluation):**

| Idea | Description |
|------|-------------|
| **A-i1** Three-state label | Replace binary "In stock" with High / Medium / Low confidence, calculated from today's POS sell-through rate, not just ERP count. Shopper sees the signal's quality, not just its value. |
| **A-i2** Staleness badge | Keep the existing label but add "Updated 8 min ago" in subdued text. Zero new ML required — just exposes the sync timestamp the system already has. Shopper calibrates trust themselves. |
| **A-i3** Friction modal at Low | At Low-confidence stores, intercept the Reserve tap with a modal: "This store may not have the item when you arrive. Choose another store?" — "Choose another" is the default action. Reservation still possible; the shopper opts in knowingly. |

---

### Theme B — Alternatives at the right moment
*How do we keep the shopper in the purchase path when their nearest store is uncertain?*

| # | HMW |
|---|-----|
| B1 | How might we help the shopper pick a more reliable store without asking them to open each store individually? |
| B2 | How might we use what we know about today's sell-through rate to surface a better option before the shopper has committed to a store? |
| B3 | How might we give the shopper a clear next step when every nearby store is uncertain — without abandoning them to the home-delivery flow? |

**Ideas (diverge — no evaluation):**

| Idea | Description |
|------|-------------|
| **B-i1** Inline alternatives section | When the nearest store is Low confidence, show 1–3 alternative stores with their confidence indicator and distance in the availability section. No navigation required; decision happens on the product page. |
| **B-i2** "Best store today" sort | Add a sort toggle to the store list: "Sorted by: Distance / Confidence today." Default to distance; let the shopper opt into confidence-first. Uses velocity signal; no UI change to the default view. |
| **B-i3** Home delivery as a peer option | When all nearby stores are Low, surface home delivery as an equal-weight option inline on the product page — not behind a delivery tab. "All nearby stores show low availability — get it delivered instead" with a one-tap path. |

---

### Theme C — Recovery when the system is wrong
*How do we rebuild trust after a failed pickup — and make the counter something other than a dead end?*

| # | HMW |
|---|-----|
| C1 | How might we turn the pickup counter from a cancellation point into a re-routing point? |
| C2 | How might we acknowledge that the system got it wrong — not just process a refund? |
| C3 | How might we make a failed pickup less likely to become a permanent defection to a competitor? |

**Ideas (diverge — no evaluation):**

| Idea | Description |
|------|-------------|
| **C-i1** Associate redirect tool | Give the associate a "find it elsewhere" lookup: when the item isn't on shelf, they can see nearby stores with confirmed stock and offer to transfer the reservation on the spot. Requires ops tooling — out of scope for product page feature but surfaces as a parallel workstream. |
| **C-i2** Proactive wrong-call email | When the confidence signal showed High and the item wasn't there: send a proactive apology email + credit, not a silent refund. "We said High confidence and we were wrong — here's what we're doing about it." Turns a trust break into a trust-building moment. |
| **C-i3** Post-cancel re-reserve link | The cancellation confirmation includes a direct link: "Reserve the same item at [highest-confidence nearby store]" — pre-populated, one tap. Converts a channel-exit moment into a recovery attempt. |

---

## Converge note

The decision (Theme A) and the retention play (Theme B) are tightly coupled: any form of signal (A-i1, A-i3) only retains shoppers if an alternative is available (B-i1, B-i3). A workshop that closes on signal design without deciding on the alternatives surface has only half-answered the question.

Sarah Chen's closing call should name: (1) signal form (label vs. modal vs. both), and (2) whether alternatives are surfaced in the same session. Everything else is implementation detail.
