---
product: Meridian click-&-collect (product detail page)
date: 2026-06-24
sources: 01-journey-map.md · Nielsen 10 heuristics · screen descriptions from brief
screens reviewed: product page (availability label) · reservation confirmation · pickup-counter email
method: AI heuristic scan → cross-checked against lived friction → findings kept only where heuristic is named + screen element is quoted
---

# Nielsen Heuristic Review: Click-and-Collect Screens

---

## Review method

Each finding required:
1. A named Nielsen heuristic (number + title)
2. A quoted screen element or observable behaviour
3. A cross-check: does this match a frustration from `01-journey-map.md`?

Findings where the AI could only say "this could be improved" without naming an element were discarded.

---

## Findings

### Screen 1 — Product Page (availability label)

---

**Finding 1.1**
- **Heuristic:** H1 — Visibility of system status
- **Element:** The availability label reads "In stock" with no timestamp, no source attribution, and no staleness indicator.
- **Violation:** The system is in a known uncertain state (SAP sync latency 15–30 min) but presents a clean, unqualified positive to the user. The label tells the shopper the system's last-known state as if it were current truth. The shopper has no way to assess whether the signal is 2 minutes or 28 minutes old.
- **Journey cross-check:** ✅ Matches F1 (step 2) — "In stock is a lie the system tells in good faith."
- **Severity:** High — this is the origin of the phantom-stock failure.

---

**Finding 1.2**
- **Heuristic:** H5 — Error prevention
- **Element:** The "Reserve for Click & Collect" button is fully enabled and uninterrupted for any stock confidence level, including borderline cases.
- **Violation:** The system has enough information to know that certain store–SKU combinations are high-cancellation-risk (from historical OMS data) but presents no friction, no warning, and no alternative at the moment the user is about to commit to the trip. Error prevention requires acting before the error occurs — here the system is silent at the last available intervention point.
- **Journey cross-check:** ✅ Matches F2 (step 3) — "commitment without certainty."
- **Severity:** High — a gate here would prevent the wasted journey.

---

**Finding 1.3**
- **Heuristic:** H2 — Match between system and the real world
- **Element:** The label "In stock" uses retailer-system vocabulary. "In stock" in ERP language means "SAP count > 0 at last sync." In shopper language it means "the item is physically on the shelf right now and I will find it there."
- **Violation:** The label exports an internal system concept into the shopper's mental model without translation. The gap between the two meanings is the entire failure surface of phantom stock.
- **Journey cross-check:** ✅ Matches F1 — the label is technically accurate and experientially misleading simultaneously.
- **Severity:** High — language fix alone narrows the expectation gap.

---

### Screen 2 — Reservation Confirmation

---

**Finding 2.1**
- **Heuristic:** H1 — Visibility of system status
- **Element:** The confirmation screen/email states "Your reservation is confirmed at [store]" with no qualification about whether the item is physically held.
- **Violation:** A reservation in Meridian's system is a booking intent, not a committed hold. The confirmation language implies the latter. The shopper's mental model after this screen is "the item is set aside for me" — which is not what the system has done. The system's actual status (logged order, no physical hold) is invisible.
- **Journey cross-check:** ✅ Matches step 4 — "reassured falsely."
- **Severity:** Medium — does not cause the phantom-stock failure but amplifies the betrayal when it occurs (the confirmation made the promise feel official).

---

**Finding 2.2**
- **Heuristic:** H3 — User control and freedom
- **Element:** The confirmation screen provides no "cancel reservation" or "choose a different store" affordance at the confirmation stage.
- **Violation:** Once the user commits, there is no clearly marked emergency exit. A shopper who has doubts after confirming must navigate away from the confirmation screen, find the order in account history, and locate a cancel flow — if one exists. There is no undo at the moment it is most needed (immediately after commitment).
- **Journey cross-check:** ✅ Matches step 4 frustration — "no cancel or re-route option at this stage."
- **Severity:** Medium.

---

### Screen 3 — Pickup-Counter Interaction (associate + shopper)

*This is not a digital screen but a system touchpoint. The violation is in what the system fails to provide to both parties.*

---

**Finding 3.1**
- **Heuristic:** H9 — Help users recognise, diagnose, and recover from errors
- **Element:** When the associate confirms the item is not on the shelf, the only system-supported outcome is "cancellation + refund offered." No alternative store lookup, no home delivery redirect, no raincheck, no reserve-at-next-available.
- **Violation:** The error is diagnosed (item not here) but the system provides no recovery path. The shopper is left to absorb the failure and exit the transaction. Recovery is the final and most important part of H9 — the system ends at diagnosis.
- **Journey cross-check:** ✅ Matches F3 (step 7) — "no recovery path at the counter."
- **Severity:** Critical — this is the channel exit point.

---

**Finding 3.2**
- **Heuristic:** H1 — Visibility of system status
- **Element:** The associate has no real-time digital inventory tool at the counter. The "system status" for the item at this store is determined by a physical shelf search.
- **Violation:** The system's actual state (stock count, last sync time, nearby-store availability) is invisible at the exact moment it would be most useful — to the person who could resolve the situation.
- **Journey cross-check:** ✅ Matches step 6 — "no digital verification tool, analog shelf search."
- **Severity:** High (associate-facing — out of scope for the current feature, flagged for ops backlog).

---

## Summary Table

| # | Screen | Heuristic | Severity | Journey step | In-scope for feature? |
|---|--------|-----------|----------|--------------|----------------------|
| 1.1 | Product page — "In stock" label | H1 Visibility of system status | High | 2 | ✅ Yes — replace with confidence signal |
| 1.2 | Product page — Reserve button | H5 Error prevention | High | 3 | ✅ Yes — warning modal at Low confidence |
| 1.3 | Product page — "In stock" label | H2 Match with real world | High | 2 | ✅ Yes — label language revision |
| 2.1 | Confirmation — "reservation confirmed" | H1 Visibility of system status | Medium | 4 | ⚠️ Partial — out of scope for Sprint 1; label language in confirmation email |
| 2.2 | Confirmation — no undo | H3 User control and freedom | Medium | 4 | ❌ Out of scope — requires reservation flow change |
| 3.1 | Pickup counter — cancellation only | H9 Recovery from errors | Critical | 7 | ⚠️ Partial — S2 (alternative stores) addresses pre-trip; counter recovery is ops scope |
| 3.2 | Pickup counter — no associate tool | H1 Visibility of system status | High | 6 | ❌ Out of scope — ops / associate tooling |

---

## Design intervention priority

Findings 1.1, 1.2, and 1.3 are the highest-leverage interventions: they address the root cause (step 2) and the last intervention point (step 3) before the shopper takes on travel cost. They are also fully within the product-page feature scope confirmed in `00-jtbd-feasibility.md`.

Finding 3.1 (no recovery at counter) is the most emotionally severe failure — but it requires S2 (alternative stores) and ops tooling. It cannot be closed by the product page feature alone.
