---
case: Meridian Retail Group — Click & Collect
feature: AI Availability Assistant — test cases
date: 2026-07-27
author: QA — Sprint 1
consumes: 600-test/00-test-plan.md
---

# Test Cases — Click & Collect AI Availability Assistant

## In-scope reference (from 00-test-plan.md)

| # | Surface |
|---|---------|
| S1 | Velocity-adjusted confidence scoring — High / Medium / Low label, SAP count × OMS sync age × POS sell-through |
| S2 | Binary fallback safety — OMS binary when model cannot score; no phantom "High" |
| S3 | Low-confidence warning modal — fires on Low; focus-trapped; absent on High / Medium |
| S4 | Velocity signal gate — POS sell-through included only if ≥ 5 % MAPE improvement; SAP-only fallback otherwise |
| S5 | Screen-reader accessibility — `aria-describedby` on label; `role="dialog"` + `aria-modal` + WCAG 2.1 AA focus trap on modal |

---

## Test case suite

| ID | Title | Surface | Category | Priority | Preconditions | Steps | Expected result | Negative? |
|----|-------|---------|----------|----------|---------------|-------|-----------------|-----------|
| TC-01 | High confidence on well-stocked Milano PDP | S1 | smoke | 1 | SAP count = 8, OMS sync age = 45 min, POS sell-through = 2 / 10 today, MAPE gate met | 1. Open Milano store PDP for SKU-JACKET-XL. 2. Observe confidence label. | Label reads "High confidence"; no modal on "Reserve" tap; reservation completes; customer leaves with item. | No |
| TC-02 | High confidence for German customer at Hamburg store | S1 | regression | 2 | SAP count = 6, OMS sync age = 30 min, POS sell-through = 1 / 8, MAPE gate met, customer locale = de-DE | 1. Open Hamburg PDP for same SKU. 2. Observe label and complete reservation. | Label reads "High confidence" in German locale; reservation accepted; store receives pickup notification. | No |
| TC-03 | Medium confidence at OMS sync boundary (3 h 59 m) | S1 | edge | 2 | SAP count = 3, OMS sync age = 3 h 59 m (just inside window), POS sell-through = 5 / 10 | 1. Open PDP. 2. Observe label. | Label reads "Medium confidence"; no fallback fires; no modal on "Reserve" tap (Medium does not trigger modal). | No |
| TC-04 | **Low confidence emitted when one unit remains and sell-through is near-total** | S1 | critical-path | 1 | SAP count = 1, OMS sync age = 2 h, POS sell-through = 9 / 10 today | 1. Open PDP. 2. Observe label. 3. Tap "Reserve". | Label reads "Low confidence"; warning modal fires; "Choose another store" receives initial focus. Customer is warned before reserving the likely-gone last unit. | **Yes** |
| TC-05 | Fallback to OMS binary when SAP sync is stale | S2 | critical-path | 1 | SAP count = 4, OMS sync age = 4 h 01 m (over threshold), POS data present | 1. Open PDP. 2. Observe label. | No confidence label rendered; UI shows OMS binary "In Stock" state; no phantom "High", "Medium", or "Low" label. | No |
| TC-06 | Fallback shows "Out of Stock" when inventory = 0 | S2 | regression | 2 | SAP count = 0 (exact zero), OMS sync age = 1 h | 1. Open PDP. 2. Observe label. | No confidence label; UI shows "Out of Stock" binary; "Reserve" CTA disabled. Customer cannot reserve a zero-stock item. | No |
| TC-07 | Negative inventory count (−2) does not produce phantom label | S2 | edge | 2 | SAP count = −2 (negative after in-store adjustment), OMS sync age = 2 h | 1. Open PDP. 2. Observe label. | No confidence label; UI shows "Out of Stock"; no phantom "In Stock" from stale OMS cache leaking through. | No |
| TC-08 | **No phantom "High" when OMS says "In Stock" but SAP = 0** | S2 | critical-path | 1 | OMS cached snapshot = "In Stock" (3 h old), SAP real-time count = 0 (depleted since snapshot) | 1. Open PDP. 2. Observe label and page state. | Model does NOT emit "High" or "Medium"; fallback fires; page shows OMS binary "In Stock" without a confidence tier label. Addresses Risk 1 directly. | **Yes** |
| TC-09 | Low-confidence modal fires with correct focus on "Reserve" tap | S3 | critical-path | 1 | SAP count = 1, OMS sync age = 1 h, POS sell-through = 8 / 10 → model scores Low | 1. Open PDP; confirm "Low confidence" label. 2. Tap "Reserve for Click & Collect". | Modal appears; `role="dialog"` present; initial keyboard focus lands on "Choose another store" button; Tab cycles within modal only (focus trapped). | No |
| TC-10 | Customer dismisses modal via "Continue anyway" and reservation completes | S3 | regression | 2 | Same as TC-09 | 1. Tap "Reserve". 2. In Low-confidence modal, tap "Continue anyway". | Modal closes; reservation flow proceeds normally; order confirmed; customer can proceed to pickup. | No |
| TC-11 | TTL re-fetch at 9 m 45 s returns Low → modal fires | S3 | edge | 2 | Score cached 9 m 45 s ago (just under 10 min TTL); re-fetch stub returns Low | 1. Wait until cached score age = 9 m 45 s. 2. Tap "Reserve". | System silently re-fetches score; re-fetch returns Low; modal fires correctly; customer is warned before stale-score reservation. | No |
| TC-12 | **TTL re-fetch timeout → modal fires as precaution (fail-safe)** | S3 | critical-path | 1 | Score cached 10 m 30 s ago; re-fetch stub times out (network error) | 1. Ensure cached score age > 10 min. 2. Tap "Reserve". | Re-fetch fails silently; system fires modal as a precautionary measure rather than allowing reservation without warning. Addresses Risk 2: fail-safe, not fail-silent. | **Yes** |
| TC-13 | Velocity signal included when POS MAPE gate is met | S4 | regression | 2 | POS sell-through data present, offline experiment shows 6 % MAPE improvement (gate met) | 1. Open PDP. 2. Inspect model inputs log (QA tool). | Model scoring uses POS sell-through rate as an input alongside SAP count and OMS sync age; confidence label reflects velocity-adjusted score. | No |
| TC-14 | SAP-only scoring when POS data is absent — no user-visible error | S4 | regression | 2 | POS sell-through stub returns no data for this store-SKU | 1. Open PDP. 2. Observe label and any error states. | Confidence label still renders (High / Medium / Low) using SAP count + OMS sync age only; no error message shown to customer; no fallback to binary unless other triggers apply. | No |
| TC-15 | MAPE gate boundary — exactly 5.0 % improvement passes | S4 | edge | 3 | POS data present; offline experiment reports MAPE improvement = 5.000 % (exact boundary) | 1. Open PDP with gate at boundary value. | Gate passes; velocity signal included in scoring; label reflects POS sell-through influence. Confirms boundary is inclusive (≥ 5 %). | No |
| TC-16 | **MAPE < 5 % → velocity signal excluded, SAP-only scoring** | S4 | regression | 2 | POS data present; offline MAPE improvement = 4.8 % (below gate) | 1. Open PDP. 2. Inspect model inputs (QA tool). 3. Observe label. | Model uses SAP-only path; POS sell-through NOT included as input; label still renders; no user-visible error. Gate correctly excludes an undertested signal. | **Yes** |
| TC-17 | VoiceOver announces confidence label via aria-describedby | S5 | smoke | 1 | iOS device with VoiceOver enabled, SKU with High confidence label rendered | 1. Navigate to PDP with VoiceOver. 2. Focus confidence label region. | VoiceOver reads "High confidence — Reserve for Click & Collect" (or locale equivalent); `aria-describedby` references the label element correctly. | No |
| TC-18 | NVDA announces Low-confidence modal structure | S5 | regression | 2 | Windows + NVDA, score = Low, "Reserve" tap pending | 1. Focus "Reserve" button with NVDA running. 2. Activate button. | NVDA announces: dialog role, modal title, body text, and the two action buttons in sequence; `aria-modal="true"` is present and NVDA does not read background content. | No |
| TC-19 | Keyboard-only navigation: focus trap holds and Escape dismisses | S5 | edge | 2 | Score = Low; modal open; keyboard-only user (no pointer) | 1. Trigger modal via keyboard Enter on "Reserve". 2. Press Tab repeatedly. 3. Press Escape. | Tab cycles within the two modal buttons only; no focus escapes to the page behind the modal; Escape closes modal and returns focus to "Reserve" button. Addresses Risk 3. | No |
| TC-20 | **Missing aria-describedby flagged by automated accessibility audit** | S5 | critical-path | 1 | Staging build with aria-describedby attribute removed from confidence label (simulates regression) | 1. Run axe-core / Lighthouse accessibility audit against the PDP. | Audit reports WCAG 2.1 AA violation SC 1.3.1 (Info and Relationships) on the confidence label element. Confirms the test suite catches an attribute regression before it reaches production. Addresses Risk 3. | **Yes** |

---

## Negative-case summary

| ID | What the system must do |
|----|------------------------|
| TC-04 | Emit Low confidence and fire modal when near-total sell-through leaves one phantom unit |
| TC-08 | Not emit a confidence tier label when OMS is stale and SAP real-time = 0; fallback only |
| TC-12 | Fire the Low-confidence modal as a precaution when re-fetch times out (fail-safe) |
| TC-16 | Exclude POS sell-through from scoring when MAPE gate is not met |
| TC-20 | Fail the accessibility audit when aria-describedby is absent |

Total negatives: **5 of 20 cases** (25 %).

---

## Coverage map

| Surface | Smoke | Critical-path | Regression | Edge |
|---------|-------|---------------|------------|------|
| S1 — Confidence scoring | TC-01 | TC-04 | TC-02 | TC-03 |
| S2 — Binary fallback | TC-05 | TC-08 | TC-06 | TC-07 |
| S3 — Low-confidence modal | TC-09 | TC-09, TC-12 | TC-10 | TC-11 |
| S4 — Velocity signal gate | — | — | TC-13, TC-14, TC-16 | TC-15 |
| S5 — Screen-reader a11y | TC-17 | TC-20 | TC-18 | TC-19 |
