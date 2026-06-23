---
product: Meridian click-&-collect (product detail page)
feature: AI availability assistant
date: 2026-06-22
status: draft v3 — full ACs (all 11 stories)
sources: 01-vision.md, 02-personas-journey.md
---

# User Stories & Acceptance Criteria

---

## Stories (8–12)

| # | Story | Priority |
|---|-------|----------|
| S1 | As a **Trip Planner**, I want to see a High / Medium / Low confidence indicator for my nearest store on the product page before I reserve, so that I can decide whether the trip is worth making without calling the store. | P0 — core AI feature |
| S2 | As a **Trip Planner**, I want to see 1–3 alternative stores with higher confidence when my nearest store shows Low, so that I can pick a better option without abandoning the purchase. | P0 |
| S3 | As a **Same-Day Seeker**, I want the confidence indicator to reflect how fast the item is selling today — not just the current count — so that "High" during a flash sale is still trustworthy. | P0 — velocity signal |
| S4 | As a **Trip Planner**, I want a clear warning before I confirm a reservation at a Low-confidence store, so that I'm not surprised by a cancellation after I've already driven there. | P0 |
| S5 | As a **Trip Planner**, I want to be offered home delivery as an alternative when all nearby stores show Low confidence, so that I don't have to abandon the purchase entirely. | P1 |
| S6 | As a **Trip Planner**, I want to see when the confidence signal was last updated, so that I can judge whether it still reflects the current shelf state. | P1 |
| S7 | As a **Trip Planner**, I want the product page to show a neutral fallback (binary in-stock status) when confidence scoring is unavailable, so that I'm never misled by a stale or fabricated confidence label. | P0 — safety |
| S8 | As a **Same-Day Seeker**, I want to compare confidence indicators across stores on a map before selecting a pickup location, so that I can choose the most reliable store without opening each one individually. | P1 |
| S9 | As a **Trip Planner with a screen reader**, I want the confidence indicator to be announced correctly by assistive technology, so that I can use the feature on equal terms. | P1 — accessibility |
| S10 | As a **Store Operations Manager**, I want to see which store–SKU combinations are generating the most Low-confidence signals, so that I can investigate root causes and improve inventory accuracy over time. | P2 — ops |
| S11 | As a **Trip Planner**, I want the confidence score shown at reservation time to be logged, so that if my order is later cancelled I can see whether the signal was accurate at the moment I reserved. | P2 |

---

## Acceptance Criteria — Top Four Stories

---

### S1 — Confidence Indicator on Product Page
*This story depends on an ML model; Gherkin cannot pin a probabilistic system. Written as AI Eval Card stub instead.*

**AI Eval Card: Velocity-adjusted collectability scoring**

| Dimension | Specification |
|-----------|--------------|
| **Model output** | Three-class confidence: High / Medium / Low, plus a numeric posterior probability (surfaced to engineering, not the shopper) |
| **Confidence thresholds** | High = posterior ≥ 0.85; Medium = 0.50–0.84; Low = < 0.50 |
| **Input signals** | SAP inventory count + same-day POS sell-through rate (units sold in last 4h at that store) + time since last OMS sync + store-SKU historical cancellation rate |
| **Refusal trigger** | Do not emit a confidence label if: (a) SAP sync is >4h stale, OR (b) same-day POS data is unavailable for the store, OR (c) inventory count = 0. Emit standard binary status instead. |
| **Latency ceiling** | p95 ≤ 800ms from product page request to confidence label rendered; must not block page render (async load) |
| **Fallback** | If model inference fails or times out: display standard binary "In stock / Out of stock" with no confidence label; log the failure; do not show a stale or cached confidence score |
| **Calibration target** | "High" correct ≥ 85% of the time (measured as: item available at pickup / total High-confidence reservations, weekly cohort); "Low" correct ≥ 70% (item unavailable at pickup / total Low-confidence reservations) |
| **False-positive penalty** | Asymmetric: a "High" that leads to a wasted trip is the primary failure mode — calibration tuning favours precision on High over recall |
| **Coverage floor** | Model must be able to score ≥ 80% of stores with sufficient POS velocity data; stores below this threshold fall back to binary status |

---

### S2 — Alternative Stores at Low Confidence

**Given** the Trip Planner views a product page for an item  
**And** the confidence indicator for their selected / nearest store is "Low"  
**When** the availability section renders  
**Then** 1–3 alternative stores are displayed below the Low-confidence indicator  
**And** each alternative shows: store name, distance from shopper's location, and its own confidence indicator  
**And** alternatives are ordered by confidence (High first, then Medium), then by distance  
**And** if no alternative store has Medium or High confidence within 30 km, the section is not shown (no false hope)  

---

### S4 — Warning Before Reserving at Low Confidence

**Given** the Same-Day Seeker has selected a store whose confidence indicator is "Low"  
**When** they tap "Reserve for Click & Collect"  
**Then** a modal is displayed before the reservation is confirmed  
**And** the modal states the confidence level in plain language: "Our system suggests this item may not be available at this store when you arrive"  
**And** the modal offers two explicit actions: "Choose another store" and "Reserve anyway"  
**And** tapping "Reserve anyway" proceeds to the standard reservation confirmation  
**And** the reservation is not placed until the shopper explicitly selects one of the two actions  
**And** the modal does not appear if the store's confidence is Medium or High  

---

### S7 — Fallback When Confidence Score Unavailable

**Given** the confidence model cannot score a store (SAP sync >4h stale, POS data unavailable, or model inference failure)  
**When** the Trip Planner views the availability section  
**Then** no confidence indicator (High / Medium / Low) is shown for that store  
**And** the standard binary inventory status ("In stock" or "Out of stock") is displayed  
**And** no "estimated" or inferred confidence label is shown  
**And** a last-updated timestamp is visible so the shopper can judge data recency  
**And** if all nearby stores are in fallback state, the full section shows binary status with a note: "Live availability estimate unavailable — stock status shown as of [timestamp]"  

---

## Adversarial Critiques (fresh session)

**S1 — Edge case:** SAP routinely produces *negative* inventory counts (returns processed against zero stock, warehouse adjustment races). A negative count passes the `count = 0` refusal guard, gets fed to the model as a legitimate signal, and emits a confidence score for stock that doesn't exist. Reservation against −3 units; failure discovered at the counter.
**S1 — NFR:** Calibration target ("High correct ≥ 85%, measured weekly") has no degradation threshold and no circuit breaker. A model that drops to 60% on Friday afternoon runs all weekend before the next review. "Correct" is also undefined — fulfilled-without-cancellation vs. confirmed-in-stock-at-pickup-time have different lag times and different semantics.

**S2 — Edge case:** "Ordered by distance" — distance from *what*? Not specified. If geolocation permission is denied, or billing address is in a different city than the shopper's physical location, "nearest" alternatives could be useless (300 miles away) while a walkable store is omitted.
**S2 — NFR:** No latency cap on the alternatives section. If alternatives require 1–3 sequential model inference calls (each up to 800ms), the section can legally take 2.4s to appear *after* the Low signal is already visible with no context. No timeout defined; the section could spin indefinitely.

**S4 — Edge case:** Confidence score is fetched at page load. A shopper who leaves the page open for hours taps "Reserve anyway" against a stale score. If stock has drained further, the modal fires correctly but warns about a now-worse situation; if restocked, the modal fires needlessly against a now-High store. Either way the modal is lying.
**S4 — NFR:** No accessibility requirements on the modal. No `role="dialog"`, no focus trap, no ARIA labels, no rule about which element gets initial focus (if "Reserve anyway" gets focus, Enter key completes the reservation accidentally). A screen reader user may never hear the warning — which is a legally material disclosure in EU consumer-protection markets.

**S7 — Edge case:** The binary fallback status shown when SAP is stale *also comes from SAP*. A shopper sees "In stock" in fallback mode and travels to the store — the exact failure mode the feature was built to prevent, now reproduced with higher trust because the UI shows a clean, unqualified positive. The AC shows a timestamp but doesn't suppress or warn.
**S7 — NFR:** No latency SLA or rate-limit protection on the fallback path. If an inference outage forces every session into fallback simultaneously, all sessions make live SAP/OMS calls that the confidence layer was caching. A model outage cascades into an inventory API brownout. No p95 defined for the fallback path, no caching requirement.

---

## ACs — Patched v2

### S1 — AI Eval Card (patched)

| Dimension | Specification (v2) |
|-----------|-------------------|
| **Model output** | Three-class confidence: High / Medium / Low, plus numeric posterior (engineering only) |
| **Confidence thresholds** | High = posterior ≥ 0.85; Medium = 0.50–0.84; Low = < 0.50 |
| **Input signals** | SAP inventory count + same-day POS sell-through (last 4h) + OMS sync age + store-SKU historical cancellation rate |
| **Refusal trigger** | Do not emit confidence label if: SAP sync >4h stale, POS data unavailable, OR **count ≤ 0** (includes negative SAP counts). Emit binary status instead. *(patch: ≤ 0, not = 0)* |
| **Latency ceiling** | p95 ≤ 800ms; async load; must not block page render |
| **Fallback** | Inference failure → binary "In stock / Out of stock", no confidence label, log failure; never show stale confidence |
| **Calibration target** | High correct ≥ 85%; Low correct ≥ 70%. Ground truth = **item physically confirmed available at pickup counter** (not "no cancellation email sent"). Measured daily on rolling 24h cohort. |
| **Circuit breaker** *(patch)* | If rolling 24h High-correctness drops below 75%: auto-revert all stores to binary fallback, page on-call. Manual re-enable required after root-cause sign-off. |
| **False-positive penalty** | Asymmetric: calibration tuning favours precision on High |
| **Coverage floor** | Model must score ≥ 80% of stores; remainder fall back to binary |

---

### S2 — Alternative Stores at Low Confidence (patched)

**Given** the Trip Planner views a product page  
**And** the selected / nearest store's confidence is "Low"  
**When** the availability section renders  
**Then** 1–3 alternative stores are displayed, each showing: store name, distance, confidence indicator  
**And** alternatives are ordered by confidence (High first, then Medium), then by distance  
**And** distance is calculated from the **shopper's current device geolocation** at render time *(patch: geolocation specified)*  
**And** if geolocation permission is denied, distance falls back to the coordinates of the currently selected store *(patch: fallback defined)*  
**And** if no alternative within 30km has Medium or High confidence, the section is not shown  

**Error path** *(patch)*: if the alternatives query fails or exceeds 400ms p95, the section is suppressed entirely (not shown as a spinner) and only the primary Low-confidence store is displayed  

**NFR** *(patch)*: alternatives must be fetched in a single batched model inference call; p95 ≤ 400ms from primary confidence render; hard timeout at 500ms after which section is hidden, not loading  

---

### S4 — Warning Before Reserving at Low Confidence (patched)

**Given** the shopper has selected a store whose confidence is "Low"  
**And** the confidence score is ≤ 10 minutes old (TTL not expired) *(patch: score TTL)*  
**When** they tap "Reserve for Click & Collect"  
**Then** a modal is displayed before reservation is confirmed  
**And** the modal states: "Our system suggests this item may not be available at this store when you arrive"  
**And** two explicit actions are shown: "Choose another store" (primary) and "Reserve anyway" (secondary)  
**And** initial keyboard focus is on **"Choose another store"** *(patch: focus management)*  
**And** the modal has `role="dialog"`, `aria-modal="true"`, focus is trapped inside, and the warning text is announced via `aria-describedby` *(patch: WCAG 2.1 AA)*  
**And** the reservation is not placed until the shopper explicitly selects one action  
**And** the modal does not appear for Medium or High confidence  

**Error path** *(patch)*: if the confidence score is >10 minutes old when the button is tapped, silently re-fetch the score before evaluating modal display; if re-fetch fails, show the modal as a precaution (fail safe, not fail silent)  

**NFR** *(patch)*: score re-validation at tap time must complete within 500ms (p95); if it exceeds this, proceed with the most recent cached score and log the staleness  

---

### S7 — Fallback When Confidence Score Unavailable (patched)

**Given** the confidence model cannot score a store (SAP sync >4h stale, POS data unavailable, or inference failure)  
**When** the Trip Planner views the availability section  
**Then** no confidence indicator is shown for that store  
**And** the binary inventory status is displayed from a **cached OMS snapshot** (not a live SAP call) *(patch: no live SAP on fallback)*  
**And** the cache TTL for the fallback snapshot is ≤ 30 minutes; cache age is shown as "last updated [timestamp]"  
**And** if the fallback trigger is specifically **SAP staleness** (sync >4h), the binary status displays: "Stock data may be outdated — check availability in store before travelling" *(patch: stale SAP fallback must warn, not silently show binary)*  
**And** if SAP data is >4h stale AND no cached snapshot is available, the store shows "Availability unknown" — not "In stock"  
**And** if all nearby stores are in fallback, a section-level note is shown: "Live availability estimates unavailable — showing last known stock status as of [timestamp]"  

**Error path** *(patch)*: partial fallback (some stores scored, some not) must be handled per-store; mixed sections are allowed; each store independently shows confidence label OR binary status as appropriate  

**NFR** *(patch)*: fallback path p95 ≤ 500ms (reads from cached snapshot, not live SAP); fallback cache must be populated by a background process, not triggered by user requests; rate-limit protection on underlying inventory API: max 1 cache-refresh request per store per 5 minutes to prevent inference-outage cascade

---

### S3 — Velocity Signal in Model

**Given** the confidence model is scoring a store  
**And** same-day POS sell-through data is unavailable for that store  
**When** the model runs  
**Then** it falls back to SAP-count + OMS sync age only (no velocity component)  
**And** the confidence label is still displayed (this is not a full fallback to binary status)  
**And** no indication is shown to the shopper that velocity data is absent  

**Error path**: if the POS snapshot is older than 4h, treat it as unavailable and score without it; if the POS feed is entirely absent for a store, the store is flagged in engineering logs but the model proceeds  

**NFR**: model must produce a score within p95 ≤ 800ms regardless of POS data availability; a missing POS signal must not increase scoring latency beyond the existing ceiling

---

### S5 — Home Delivery Fallback at All-Low Stores

**Given** the Trip Planner views a product page  
**And** all stores within 30km of the shopper show Low confidence  
**When** the availability section renders  
**Then** a home delivery option is displayed as an alternative  

**Error path**: if home delivery is also unavailable (item out of stock online) — do not show the home delivery option; never display a home delivery link that leads to an out-of-stock state  

**NFR**: home delivery availability check must run as a parallel fetch alongside confidence scoring; must not add sequential latency; contribution to total availability section render time ≤ 200ms p95

---

### S6 — Signal Recency Timestamp

**Given** the confidence label is shown for a store  
**When** the availability section renders  
**Then** a timestamp is displayed showing when the confidence signal was last calculated  
**And** the timestamp format is: "Updated [time] today" or "Updated [date] at [time]" (local timezone)  

**Error path**: if the signal timestamp cannot be determined (OMS sync metadata missing) → suppress the timestamp entirely; do not display a default, zero, or fabricated time  

**NFR**: timestamp is included in the same async payload as the confidence label; adds zero additional network calls or rendering latency

---

### S8 — Store Map with Confidence Indicators

**Given** the shopper is in the store-selector view  
**When** the map renders  
**Then** each store pin is overlaid with its confidence indicator (High / Medium / Low or fallback indicator)  
**And** tapping a pin shows the store name, distance, and confidence label  

**Error path**: if device geolocation is denied or unavailable → map centers on the shopper's billing postcode; if billing postcode is also unknown, map centers on the nearest city associated with the selected store; confidence overlays still display regardless of geolocation state  

**NFR**: map with confidence overlays must render within p95 ≤ 1.2s from user interaction; confidence overlays are fetched in a single batched call; map tile loading is independent of confidence data (tiles render first, overlays populate when ready)

---

### S9 — Screen Reader Accessibility
*Quality attribute of S4 — baked into S4 delivery cost. No standalone metric link.*

**Given** the shopper uses a screen reader  
**When** the confidence label renders on the product page  
**Then** the label is announced as: "[High / Medium / Low] confidence for click-and-collect at [store name]"  
**And** when the Low-confidence warning modal opens, focus moves to the modal heading and the warning text is announced via `aria-describedby`  

**Error path**: if the `aria-live` region is not supported by the assistive technology → confidence label and modal warning remain reachable via standard tab-order keyboard navigation; the modal must be focusable without relying on live announcements  

**NFR**: WCAG 2.1 AA compliance verified against VoiceOver (iOS/macOS) and NVDA (Windows) before release; `role="dialog"`, `aria-modal="true"`, focus-trapped, `aria-describedby` on modal warning text — all verified in S4 delivery

---

### S10 — Ops Monitoring Dashboard
*Icebox — schedule review after 90 days of S1 data.*

**Given** a Store Operations Manager opens the monitoring dashboard  
**When** the dashboard loads  
**Then** a ranked table is shown of store–SKU combinations by Low-confidence signal count over the past 7 days  
**And** each row shows: store name, SKU, Low-signal count, cancellation rate for that store–SKU, and last updated time  

**Error path**: if the data pipeline lag exceeds 24h → a warning banner is shown: "Data as of [last-confirmed-date] — pipeline delayed"; never silently display stale data as current  

**NFR**: dashboard data refreshes on a ≤ 4h schedule; dashboard is read-only (no data modifications via this UI); data must be exportable as CSV; access restricted to ops role

---

### S11 — Log Confidence Score at Reservation

**Given** a shopper confirms a click-and-collect reservation  
**When** the reservation API call completes  
**Then** the confidence score shown at the time of reservation (label + numeric posterior) is written to the confidence event log  
**And** the log entry includes: reservation ID, store ID, SKU, confidence label, posterior value, model version, signal timestamp  

**Error path**: if the logging service is unavailable when the reservation fires → the reservation still completes without delay; the log entry is queued for async retry (max 3 attempts within 1 hour); if all retries fail, the entry is written with status "confidence data unavailable" and flagged for manual recovery  

**NFR**: logging write is fire-and-forget; must add zero latency to the reservation API response (p99 contribution ≤ 0ms); logging failure must never cause a reservation failure
