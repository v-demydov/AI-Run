---
product: Meridian click-&-collect (product detail page)
date: 2026-06-24
sources: 03-decision.md · 04-stories-acs.md (S1 AI Eval Card v2)
decided-change: Three-state confidence label (A-i1) + friction modal at Low (A-i3)
---

# AI Acceptance Criteria: Availability Confidence Feature

---

## User Story

**As a** click-and-collect shopper deciding whether to make a pickup trip,
**I want** to see how confident the system is that the item will be physically on the shelf at my chosen store before I confirm the reservation,
**so that** I only commit to the trip when the signal is trustworthy — and I can redirect to a better store when it isn't, before I leave home.

---

## Base AC (supplied — happy path + empty states)

| # | Condition | Expected behaviour |
|---|-----------|-------------------|
| AC1 | WHEN a product has store stock data | THEN the product page shows an availability indicator per nearby store |
| AC2 | WHEN no store within range has the item | THEN show "Not collectable nearby" + a delivery option |
| AC3 | WHEN stock data is missing for a store | THEN omit that store — do not guess |
| AC4 | WHEN the user taps a store | THEN show last-confirmed time + distance |

---

## AI-Specific AC

---

### AI-AC1 — Confidence (what the label claims must be measurably true)

**WHEN** the system displays a "High" confidence label for a store–SKU combination,
**THEN** the item must be physically confirmed available at the pickup counter for
≥ 85% of reservations placed under that label,
measured as a rolling 24-hour cohort (reservations made in window T, pickups confirmed in window T + pickup-lead-time).

If the observed High-correctness rate in any rolling 24-hour window drops below **75%**,
the circuit breaker fires automatically: all stores revert to binary fallback (AC2/AC3 path),
an on-call alert is raised, and the feature remains in fallback until a root-cause review
is completed and a human manually re-enables it.

*Threshold summary: High-correctness target ≥ 85%; circuit-breaker floor 75%; window 24h rolling.*

---

### AI-AC2 — Refusal / Fallback (when the model must not emit a label)

**WHEN** any of the following conditions are true for a store:
- SAP inventory sync age > 4 hours, **OR**
- Same-day POS sell-through data is unavailable for that store, **OR**
- Inventory count ≤ 0 (including negative SAP counts)

**THEN** the confidence model must NOT emit a High / Medium / Low label.
The store must display the binary status ("In stock" / "Out of stock") read from the **cached OMS snapshot** (not a live SAP call).

If the OMS snapshot is also unavailable:
- The store must show **"Availability unknown"** — never a clean "In stock" positive.
- If SAP staleness is the trigger (>4h), the binary status must include a visible notice:
  "Stock data may be outdated — check availability in store before travelling."

*Threshold summary: refusal triggers at SAP age >4h, missing POS data, or count ≤ 0; fallback source = cached OMS snapshot ≤ 30 min old.*

---

### AI-AC3 — Latency (the label must not make the page slow)

**WHEN** the product page loads,
**THEN** the confidence label must render within **p95 ≤ 800ms** from the moment the product page makes the confidence API request.

The label must load **asynchronously** — the product page must not block on the confidence API. The page content (images, price, description) must be interactive before the confidence label appears.

If the inference call does not return within **1 000ms** (hard client-side timeout),
the fallback binary status must render automatically without any user action.
An alert must be logged; no spinner must spin indefinitely.

*Threshold summary: label p95 ≤ 800ms async; hard timeout 1 000ms → auto-fallback.*

---

### AI-AC4 — Disclosure (the label must not claim more than the system knows)

**WHEN** a High / Medium / Low confidence label is displayed,
**THEN:**

1. The label must show the signal age: **"Updated [N] min ago"** — calculated from the OMS sync timestamp, displayed adjacent to or within the label.

2. The label copy must use **non-guarantee language**. Required copy forms:
   - High → "Likely available"
   - Medium → "May vary — check before travelling"
   - Low → "May not be available"

3. The following phrases are **forbidden** in the label or modal:
   - Any form of "guaranteed", "confirmed in stock", "reserved for you", "we're holding it"
   - Any language that implies a physical inventory hold has been created.

4. The friction modal (Low stores) must repeat the plain-language copy and include the signal age.

*Observable test: a QA reviewer reads the label and modal copy; any language implying a committed hold is a failing condition.*

---

### AI-AC5 — Feedback (the system must be able to learn from its errors)

**WHEN** a shopper confirms a click-and-collect reservation,
**THEN** the following data must be written to the confidence event log within **1 second** of reservation confirmation:
- Reservation ID, Store ID, SKU
- Confidence label shown at reservation time (High / Medium / Low)
- Numeric posterior probability
- Model version
- OMS sync timestamp used for that inference

The logging write must be **fire-and-forget** — a logging failure must never block or delay the reservation confirmation response.

This log is the sole input for computing the rolling 24h High-correctness rate used by AI-AC1's circuit breaker. If the log is unavailable for >2 hours, the circuit breaker must treat High-correctness as **unknown** and auto-revert to fallback until logging is restored.

*Threshold summary: log write within 1s; fire-and-forget; logging outage >2h triggers circuit breaker.*

---

### AI-AC6 — Negative AC (what the system must never do)

The following conditions are **absolute prohibitions** with no override:

| Prohibition | Condition that would trigger it (and must not) |
|-------------|------------------------------------------------|
| Must NOT display "High" | SAP count ≤ 0 for that store–SKU |
| Must NOT display "High" | SAP sync age > 4h for that store |
| Must NOT display "High" | Rolling 24h High-correctness < 75% |
| Must NOT display any confidence label | When the OMS snapshot age > 30 min (show "Availability unknown" instead) |
| Must NOT imply a physical hold exists | At any confidence level — no "we're holding it" copy |
| Must NOT substitute a confidence label for a cancellation | If OMS has already flagged the order as cancelled, the confidence label must not re-assert availability |

*Test method: each prohibition is a separate QA test case; any single violation is a release blocker.*

---

## Falsifiability check

| Clause | Threshold present? | Observable / testable? |
|--------|--------------------|----------------------|
| AI-AC1 | ≥ 85% target; 75% circuit-breaker floor; 24h window | ✅ Computable from event log |
| AI-AC2 | >4h SAP age; ≤ 0 count; missing POS | ✅ Each condition is a Boolean test |
| AI-AC3 | p95 ≤ 800ms; hard timeout 1 000ms | ✅ Load-test measurable |
| AI-AC4 | Forbidden phrase list; signal age display | ✅ Copy review + DOM inspection |
| AI-AC5 | 1s log write; 2h outage trigger | ✅ Integration test + monitoring alert |
| AI-AC6 | Explicit prohibition table | ✅ Each row is a separate test case |
