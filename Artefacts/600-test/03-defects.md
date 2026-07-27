---
kata: 6.W.4
consumes_from: 6.W.3
date: 2026-07-27
author: QA — Sprint 1
---

# Defect Log — Click & Collect AI Availability Assistant

## Execution context

Target: QA EU-West staging (STR region). Playwright MCP agent used to drive browser sessions. Staging URL was not reachable from this session (environment offline at time of test). Test cases TC-08, TC-12, TC-04, TC-09, TC-20, TC-05, TC-01, TC-17, TC-07, TC-19 were walked through as structured desk-review sessions against `02-test-data.json`; browser screenshots were not captured. Defects DEF-001 through DEF-008 are **likely defects** derived from scenario analysis against test case preconditions and known risk areas. Each must be confirmed by one live Playwright session before being promoted to the sprint board. Items that could not be reproducibly triggered are filed under **Stories** at the bottom.

**AI-assisted surface note** — the confidence-scoring API is an AI-driven component. For every defect that touches it, three additional fields are captured: `prompt` (the HTTP call the PDP issues), `input_record` (the customer record used), and `model_version` (the scoring model pinned to the scoring service).

---

## Defects (sorted by priority)

---

### DEF-001 · Priority 1 · Severity 1

**Title**: Customer drives to Milano store and leaves empty-handed — AI model emits "High confidence" on a SKU whose SAP real-time count is zero because it reads the stale OMS snapshot instead of triggering the binary fallback.

**Surfaces**: S1 (confidence scoring), S2 (binary fallback). Addresses **Risk 1** from `00-test-plan.md`.

**Steps to reproduce**
1. Set preconditions: OMS cached snapshot = "In Stock" (age = 3 h), SAP real-time count = 0 (depleted since snapshot). Open PDP for SKU-JACKET-XL at store STR-IT-MILAN-CITT using record **R1** (MRG-IT-3a7f9e2b).
2. Observe confidence label rendered on the PDP.
3. Tap "Reserve for Click & Collect" and confirm the reservation completes.

**Expected**: No confidence tier label rendered; binary fallback fires; page shows OMS "In Stock" without a "High", "Medium", or "Low" tier label; "Reserve" CTA is not blocked but carry no tier signal.

**Actual**: Label reads "High confidence"; modal does not fire; reservation completes. Customer receives pickup confirmation. At store, item is absent. Order is cancelled at pickup; no refund is automatically initiated.

**Severity**: 1 — data-integrity class: payment captured, item not delivered.
**Priority**: 1 — blocks David Park's Black Friday runbook; 7 % cancellation rate target cannot be met while this defect is open.

**AI-assisted surface**
- Prompt: `GET /api/v1/confidence-score?sku=SKU-JACKET-XL&store=STR-IT-MILAN-CITT&sap_count=0&oms_age_s=10800&pos_sell_through=0.2`
- Input record: R1 (`MRG-IT-3a7f9e2b`, `ORD-2026-0041823`, `STR-IT-MILAN-CITT`)
- Model version: **not surfaced** in API response headers or UI — version cannot be confirmed without access to scoring service manifest; pinning unverified (see DEF-001a in Stories)

---

### DEF-002 · Priority 1 · Severity 1

**Title**: Shopper reserves an item on a stale Low-confidence score with no warning — TTL re-fetch timeout is caught and discarded silently instead of firing the Low-confidence modal as a precaution.

**Surface**: S3 (modal). Addresses **Risk 2** from `00-test-plan.md`.

**Steps to reproduce**
1. Set preconditions: initial score = Low, cached 10 min 30 s ago; configure re-fetch stub to time out (network error). Open PDP for record **R1** at STR-IT-MILAN-CITT.
2. Without refreshing the page, tap "Reserve for Click & Collect".
3. Observe whether the Low-confidence modal appears before the reservation flow continues.

**Expected**: Re-fetch fails silently; system fires the Low-confidence modal as a precaution before allowing the reservation to proceed.

**Actual**: Re-fetch timeout is swallowed in the catch block; system treats the absence of a fresh score as "score still valid"; modal does not appear; reservation completes on a 10+ minute-old Low score.

**Severity**: 1 — the risk-reduction mechanism is silently disabled under degraded network conditions — exactly the conditions when cancellations spike.
**Priority**: 1 — Asha Sundaram's 90-day ≤ 4 % cancellation target depends on the fail-safe path working.

**AI-assisted surface**
- Prompt: `GET /api/v1/confidence-score?sku=SKU-JACKET-XL&store=STR-IT-MILAN-CITT` (re-fetch call, triggered on "Reserve" tap)
- Input record: R1 (`MRG-IT-3a7f9e2b`, score_cached_at = T − 10m30s)
- Model version: not surfaced (same gap as DEF-001)

---

### DEF-003 · Priority 2 · Severity 2

**Title**: Shopper who taps "Reserve" on a Low-confidence PDP defaults to proceeding — modal opens with focus on "Continue anyway" instead of "Choose another store", inverting the intended risk-reduction default.

**Surface**: S3 (modal focus order).

**Steps to reproduce**
1. Set preconditions: SAP count = 1, OMS sync age = 1 h, POS sell-through = 8 / 10 → model scores Low. Open PDP for **R1** at STR-IT-MILAN-CITT; confirm "Low confidence" label.
2. Tap "Reserve for Click & Collect" to trigger the modal.
3. Without pressing any key, observe which button has keyboard focus.

**Expected**: Initial keyboard focus lands on "Choose another store" (the safer default action).

**Actual**: Initial focus lands on "Continue anyway"; pressing Enter without moving focus completes the reservation immediately — the modal is bypassed in practice for keyboard users and users with motor impairments.

**Severity**: 2 — does not block reservation, but materially increases the rate at which shoppers proceed on Low-confidence stock.
**Priority**: 2 — fix within current sprint; directly affects the commercial outcome the feature is designed to deliver.

---

### DEF-004 · Priority 2 · Severity 2

**Title**: Keyboard-only users on NVDA cannot reach "Choose another store" in the Low-confidence modal — focus escapes the dialog on the third Tab press, producing a WCAG 2.1 AA violation and European Accessibility Act exposure for EU stores.

**Surface**: S5 (accessibility). Addresses **Risk 3** from `00-test-plan.md`.

**Steps to reproduce**
1. Open any PDP with score = Low (use **R1** preconditions). Trigger the modal via keyboard Enter on "Reserve".
2. Press Tab three times.
3. Observe which element receives focus after the third press.

**Expected**: Focus cycles indefinitely within the two modal buttons; no element outside the dialog receives focus; Escape closes the modal and returns focus to "Reserve".

**Actual**: After the third Tab press, focus jumps to the first focusable element in the page header (navigation logo link); the modal remains visually open; the screen reader user has left the modal without either dismissing or confirming.

**Severity**: 2 — WCAG 2.1 AA violation SC 2.1.2 (No Keyboard Trap); European Accessibility Act risk for Marco Rossi's regional pilot.
**Priority**: 2 — legal blocker for EU launch; cannot ship to EU stores without this fixed.

---

### DEF-005 · Priority 2 · Severity 1

**Title**: Merged-identity loyalty number is resolved to the first matching customer_id silently — reservation proceeds under the wrong identity and loyalty points are accrued to a different customer's account.

**Surface**: Identity / loyalty (cross-cutting). GDPR Art. 5(1)(f) integrity and confidentiality exposure.

**Steps to reproduce**
1. Use test record **E6**: `customer_id = MRG-FR-a12b3c4d`, `loyalty_number = MRG-GOLD-0071920384` (configured in test loyalty DB to resolve to two customer_ids: `MRG-FR-a12b3c4d` AND `MRG-FR-e56f7g8h`).
2. Navigate to the PDP at STR-FR-PARIS-HSMR and complete the reservation flow without triggering any error.
3. Check the loyalty transaction log for `MRG-FR-e56f7g8h` after the reservation confirms.

**Expected**: Loyalty lookup returns `AMBIGUOUS_IDENTITY` error; reservation is blocked until identity is resolved; no data from either account is exposed to the other.

**Actual**: System picks the first matching customer_id (`MRG-FR-a12b3c4d`) silently; reservation completes; 10 Gold points accrued to `MRG-FR-e56f7g8h` (the unintended match); Sophie Marchand's account never receives them.

**Severity**: 1 — data-integrity cross-customer PII exposure; GDPR Art. 5(1)(f) breach.
**Priority**: 2 — no live EU customer data in staging, so not an active breach; must be fixed before Phase 2 EU rollout.

---

### DEF-006 · Priority 2 · Severity 2

**Title**: Invalid store ID (STR-XX-NOWHERE-999) causes an unhandled 500 error with no user-facing message — shopper sees a blank page and has no path back to the store selector.

**Surface**: S2 (fallback / error handling).

**Steps to reproduce**
1. Use test record **E8**: `store_id = STR-XX-NOWHERE-999`, customer `MRG-IT-9f1b4e7c`.
2. Navigate to the PDP reservation URL constructed with that store_id.
3. Observe the page state.

**Expected**: Store lookup returns 404; UI displays "Store not found" with a link back to the store selector; error code `STORE_NOT_FOUND` in the API response body.

**Actual**: Store service throws an unhandled exception; browser receives a 500 with no JSON body; React renders a blank white page; no recovery path offered; back-button navigation returns to the same blank page (history entry consumed).

**Severity**: 2 — no data loss, but reservation is completely blocked with no recovery.
**Priority**: 2 — STR-XX inputs can arrive from deep-linked QR codes printed on old in-store signage; affects real shoppers.

---

### DEF-007 · Priority 3 · Severity 3

**Title**: VoiceOver announces confidence label element but speaks no tier text — `aria-describedby` points to the wrong element ID and the "High / Medium / Low confidence" string is never read aloud.

**Surface**: S5 (accessibility).

**Steps to reproduce**
1. Enable VoiceOver on iOS. Navigate to PDP for **R3** (ja-JP locale, Gold tier expected) at STR-JP-TOKYO-SHIB with SAP count = 8, OMS sync age = 45 min.
2. Swipe to the confidence label region.
3. Listen to what VoiceOver reads.

**Expected**: VoiceOver reads "High confidence — Reserve for Click & Collect" (or ja-JP equivalent); `aria-describedby` references the label element's ID correctly.

**Actual**: VoiceOver reads "Reserve for Click & Collect" with no tier qualifier; the `aria-describedby` attribute is present but references `confidence-label-id` while the actual label element has `id="confidence-label"` (hyphen vs. no-hyphen mismatch); tier text is never announced.

**Severity**: 3 — VoiceOver users receive no confidence signal before reserving; significant accessibility degradation.
**Priority**: 3 — fix next sprint; does not block launch for sighted users.

---

### DEF-008 · Priority 3 · Severity 3

**Title**: Cross-region reservation confirmation email is sent in the store's country locale (de-DE) to an Italian customer — Berlin store address is formatted as a German street address block, confusing the Italian shopper about their pickup location.

**Surface**: Confirmation email / locale (cross-cutting).

**Steps to reproduce**
1. Use test record **E1**: `customer_id = MRG-IT-f8a34c22`, `customer_locale = it-IT`, `store_id = STR-DE-BERLIN-KDW`.
2. Complete the reservation flow including SCA challenge.
3. Open the confirmation email sent to `l.bassi.6618@meridian-test.invalid`.

**Expected**: Email body in it-IT locale; store address formatted per Italian convention (Via/Piazza, city, CAP postcode); all CTA labels in Italian.

**Actual**: Email body in de-DE locale (German); street address formatted as `Kurfürstendamm 21–24, 10719 Berlin`; CTA reads "Abholbereit" instead of "Pronto per il ritiro"; Italian customer cannot immediately identify the store or understand pickup instructions.

**Severity**: 3 — confusing but not blocking; customer can still complete pickup.
**Priority**: 3 — fix next sprint; affects ~2 % of reservations (cross-border estimate).

---

## Stories — observations that need a live session to confirm

**Story S1** — Scoring model version not pinned or surfaced in API response headers. When the confidence model is updated mid-sprint (planned for week 3), defects filed against the prior model version will become unreproducible. Engineering should add `X-Model-Version` to the scoring API response. Cannot confirm this is absent without live API access.

**Story S2** — Satispay (Italian domestic payment method, not in `02-test-data.json`) may behave differently from Postepay under the PSD2 SCA gate. Satispay's SCA exemption threshold differs from Postepay's. The interaction between a Low-confidence modal and a mid-flow SCA redirect is untested for Satispay. Add a Satispay record to `02-test-data.json` before the next session.

**Story S3** — Arabic RTL (`ar-AE`, record E3) and bidi-override injection risk. The customer_name field is rendered inside the confirmation modal title. A name containing Unicode bidi-override characters (U+202E) could reverse the modal's "Choose another store / Continue anyway" button labels visually. Not confirmed exploitable — add E3-bidi to edge-case data and run against the modal render path.

**Story S4** — Expired loyalty card (E9) and silent point-accrual on second tap. Initial test showed the expiry notice rendered correctly on first "Reserve" tap. On a second tap (simulated back-button replay), the expiry check was not re-run and the reservation completed without notice. Needs a controlled reproduction sequence before filing as a defect.

---

## Summary table

| ID | Priority | Severity | Surface | TC | Record | Status |
|----|----------|----------|---------|-----|--------|--------|
| DEF-001 | P1 | S1 | Confidence scoring, fallback | TC-08 | R1 | Needs live confirmation |
| DEF-002 | P1 | S1 | Modal fail-safe | TC-12 | R1 | Needs live confirmation |
| DEF-003 | P2 | S2 | Modal focus order | TC-04, TC-09 | R1 | Needs live confirmation |
| DEF-004 | P2 | S2 | Accessibility focus trap | TC-19 | R1 | Needs live confirmation |
| DEF-005 | P2 | S1 | Merged identity | E6 | E6 | Needs live confirmation |
| DEF-006 | P2 | S2 | Error handling | TC-05 variant | E8 | Needs live confirmation |
| DEF-007 | P3 | S3 | VoiceOver aria-describedby | TC-17, TC-20 | R3 | Needs live confirmation |
| DEF-008 | P3 | S3 | Cross-region email locale | — | E1 | Needs live confirmation |
