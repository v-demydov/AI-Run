---
kata: 6.W.5
consumes_from: 6.W.4
date: 2026-07-27
defect: DEF-001
---

# Root Cause Analysis — DEF-001

---

## 1. Defect summary (from 03-defects.md)

**Title**: Customer drives to Milano store and leaves empty-handed — AI model emits "High confidence" on a SKU whose SAP real-time count is zero because it reads the stale OMS snapshot instead of triggering the binary fallback.

**Surfaces**: S1 (confidence scoring), S2 (binary fallback). Addresses Risk 1 from `00-test-plan.md`.

**Steps to reproduce**
1. Set preconditions: OMS cached snapshot = "In Stock" (age = 3 h), SAP real-time count = 0 (depleted since snapshot). Open PDP for SKU-JACKET-XL at store STR-IT-MILAN-CITT using record R1 (MRG-IT-3a7f9e2b).
2. Observe confidence label rendered on the PDP.
3. Tap "Reserve for Click & Collect" and confirm the reservation completes.

**Expected**: No confidence tier label rendered; binary fallback fires; page shows OMS "In Stock" without a tier label.

**Actual**: Label reads "High confidence"; reservation completes; customer arrives at store; item is absent; order cancelled at pickup.

**Severity**: 1. **Priority**: 1.

---

## 2. Root cause hypotheses

The system: commercetools order layer → Apollo GraphQL BFF → SAP ECC read-only sync → confidence-scoring model. Per `00-test-plan.md` the binary fallback is triggered by ANY of: (a) POS data absent, (b) OMS sync age > 4 h, or (c) inventory ≤ 0. In the failing scenario OMS age = 3 h (condition b not met), SAP count = 0 (condition c should be met), yet the model emits "High" instead of deferring to fallback.

**H1 — OMS freshness gate short-circuits the SAP count ≤ 0 check (strongest)**  
Condition: The scoring model evaluates the OMS binary signal first. When OMS reports "In Stock" AND OMS age is within the 4-hour window, the model treats the item as scoreable and skips the `sap_count ≤ 0` guard entirely — entering the scoring path with a zero count as if it were a valid positive quantity.  
Confirm: In the scoring model's decision tree (or GraphQL resolver), check whether the `sap_count ≤ 0` branch sits inside the `oms_age < 14400s` block rather than before it.  
Rule out: If `sap_count ≤ 0` is evaluated unconditionally as the first gate before any OMS check, this hypothesis fails.

**H2 — Scoring model reads the SAP count written at OMS sync time, not real-time**  
Condition: The SAP ECC count stored in the commercetools product variant is the value captured at the last OMS sync (3 h ago, when count was > 0). The scoring service reads this cached field rather than issuing a live SAP call, so it sees a stale positive count.  
Confirm: Compare the `sap_quantity` timestamp in the scoring API request payload against the OMS snapshot timestamp — if they are the same, the scoring model is reading the OMS-cached SAP value.  
Rule out: If the scoring service issues a direct SAP ECC call (separate from the OMS sync path) at score-time, the timestamps will differ.

**H3 — SAP null vs zero conflation in the depleted-stock response**  
Condition: SAP ECC returns `null` (no record) rather than `0` when inventory is fully depleted and the item falls below the minimum-stock threshold for the store. The `sap_count ≤ 0` guard checks only for integer zero and negative; null passes through as "data unavailable" and the model scores on a null count.  
Confirm: Capture the raw SAP BAPI response for a depleted SKU; check whether the quantity field is `0` or absent/null.  
Rule out: If SAP always returns an integer (including 0) for any queried store-SKU pair, null conflation is not the cause.

**H4 — Race: reservation write commits after scoring API reads**  
Condition: The last unit was reserved by another customer 10–30 seconds before this session opened the PDP. The scoring model's SAP read ran before that reservation was committed to the SAP delta feed, so it saw count = 1, scored "High", and cached the result. The PDP renders the cached score (count = 1 at cache-write time) while SAP now holds count = 0.  
Confirm: Check whether phantom "High" emissions correlate with recent (< 60 s) reservations at the same store-SKU in the activity log.  
Rule out: Reproduce the defect with a clean fixture where SAP count is set to 0 before any session begins — if the phantom label still appears, the race is not required.

**H5 — Wrong field: scoring reads `quantity_on_hand`, guard checks `quantity_available`**  
Condition: SAP ECC exposes two distinct inventory fields: `quantity_on_hand` (physical units) and `quantity_available` (net of open reservations). The scoring service reads `quantity_on_hand` (which is 0), but the fallback guard evaluates `quantity_available` (which may still be positive due to a stale reservation offset). The guard never fires because it never sees the zero.  
Confirm: Inspect the GraphQL schema mapping between the SAP integration layer and the scoring service — check which field each path consumes.  
Rule out: If the integration layer exposes only a single `sap_count` field (mapping hidden behind the BFF), the field-split cannot occur.

**Chosen hypothesis: H1** — it is the only hypothesis that explains why the defect occurs even in a clean fixture (no race, no field split, no null) and is consistent with the OMS age being inside the freshness window. H2 is possible but would manifest as a staleness regression across all stores, not selectively; H3 and H5 require SAP integration quirks that are unconfirmed; H4 is a race scenario the test plan's own Risk 1 description treats as a distinct problem.

---

## 3. Root cause

**The condition that made this bug possible was that the confidence-scoring model evaluated the OMS binary signal before the SAP count, and when OMS reported "In Stock" within the 4-hour staleness window, the model entered the scoring path directly — bypassing the `sap_count ≤ 0` fallback gate — so a real-time SAP count of zero was passed to the scoring function as a valid positive quantity and scored "High".**

---

## 4. Guard test

The instance: `STR-IT-MILAN-CITT`, `SKU-JACKET-XL`, OMS age = 3 h, SAP = 0.  
The condition: OMS "In Stock" within the 4-hour window bypasses the SAP ≤ 0 gate.  
The guard test exercises three other inputs where the same condition can hold — a different region, a different SKU class, and the tightest possible OMS freshness value — to prevent the bug returning through a neighbouring input.

---

| ID | Title | Surface | Category | Priority | Preconditions | Steps | Expected result | Negative? |
|----|-------|---------|----------|----------|---------------|-------|-----------------|-----------|
| TC-GRD-01 | **SAP count = 0 with fresh OMS snapshot must suppress all confidence tier labels across region, SKU class, and OMS age** | S1, S2 | guard | 1 | Three fixtures run in sequence. **Fixture A** — STR-DE-HAMBURG-EZE, SKU-JACKET-XL, OMS age = 30 min (very fresh), SAP count = 0. **Fixture B** — STR-JP-TOKYO-SHIB, SKU-SCARF-OS (accessories class), OMS age = 3 h 59 m (maximum freshness before stale threshold), SAP count = 0. **Fixture C** — STR-GB-LONDON-KNB, SKU-DRESS-M, OMS age = 10 min (just synced), SAP count = 0. MAPE gate met in all three; POS data present; no recent reservations against these store-SKU pairs. | 1. For each fixture, open the PDP and observe the confidence label. 2. Tap "Reserve for Click & Collect" and observe whether the reservation flow proceeds. 3. Inspect the scoring API response body for `tier`, `fallback_reason`, and `sap_count` fields. | **All three fixtures**: (a) no confidence tier label rendered on the PDP; (b) UI shows OMS binary "In Stock" without a "High", "Medium", or "Low" qualifier; (c) the "Reserve" CTA is present but no tier signal accompanies it; (d) scoring API response body contains `"tier": null, "fallback_reason": "sap_count_zero", "sap_count": 0`. If any fixture emits a tier label or the `fallback_reason` field is absent, the guard fails and the condition is confirmed active. | **Yes** |

---

## 5. Fix recommendation

**Restructure the scoring model's entry gate so that `sap_count ≤ 0` is evaluated as an unconditional pre-check — before any OMS signal is read — and routes directly to the binary fallback path, making zero or negative inventory a hard stop that no OMS freshness state can override.**
