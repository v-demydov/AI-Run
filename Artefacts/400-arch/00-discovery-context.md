---
case: Meridian Retail Group
kata: 4.W.1
date: 2026-06-25
sources: 100-Wide/01-Context-brief.md · 200-PRD/06-prd.md · 200-PRD/04-stories-acs.md · 300-design/06-context.md · 300-design/06-spec.md
self-contained: yes — paste this file alone into a fresh session to reason about architectural options
---

# 00 — Discovery Context: Meridian Omnichannel Platform

---

## Business layer

- **Programme:** $42M, 18-month board-approved initiative to merge 22 regional commerce stacks. Immediate feature in scope: AI Availability Assistant for click-and-collect product pages.
- **Quantified pain:** 12% phantom stock on click-and-collect = €8M/year in cancelled pickups + customer defection to Zalando/ASOS. 35% of repeat customers treated as new across 3 fragmented loyalty systems = €12M/year in lost upsell. Total addressable margin: ~€20M/year.
- **Competitive pressure:** Zalando, ASOS, and Inditex each report <3% phantom stock after investing in unified inventory. Customers who experience one failed pickup defect. Every 1% phantom stock reduction = ~€667K recovered margin.
- **Success measure (locked):** C&C cancellation-at-pickup rate 7% → ≤4% in 90 days post-launch. Reservation conversion rate must not drop >1 pp (guardrail — not a growth target).
- **Stakeholder tension:** Regional GMs control their storefront deployments and resist central consolidation, citing local language and local payment-method requirements. This is a governance risk that has no resolution documented in the brief.

---

## Product layer

- **Primary surface:** Product detail page, availability section — the moment a shopper decides whether a pickup trip is worth making. Async confidence signal loads after page render; must never block it.
- **User moments covered in Sprint 1:** (1) Pre-reservation — three-state confidence label (High / Medium / Low) on the product page. (2) Reservation gate — FrictionModal intercepts the Reserve tap when the selected store is Low, defaulting focus to "Choose another store."
- **Channels:** Online reservation (mobile primary, desktop secondary) → in-store physical pickup at one of 600 EU stores. The confidence signal is a pre-trip decision aid, not a committed hold.
- **Deferred surfaces (P1/P2, post-S1 evidence gate):** Alternative stores at Low confidence (S2), home delivery fallback (S5), store map with confidence overlays (S8), ops monitoring dashboard (S10). None are in scope for this architecture pack's Sprint 1 contracts.

---

## Engineering layer

- **Fragmented storefront estate:** Three separate deployments — Shopify Plus (DE/AT), custom .NET (IT), Magento 2 (FR/ES). The confidence feature must surface on all three. No BFF or unified API gateway is documented in the brief as existing today.
- **Inventory pipeline:** SAP S/4HANA is the inventory source of truth; it batch-syncs to the OMS with a 2–4h lag during peak. POS velocity (600 stores, mixed vendors) is aggregated to OMS on a daily schedule — not in real-time. There is no documented live SAP query API or sub-4h POS feed.
- **Target architecture (locked in design katas):** Dedicated Confidence API microservice (async, p95 ≤ 800ms); OMS snapshot cache (Redis, TTL ≤ 30min) for fallback reads — never live SAP on the fallback path; ML scoring engine consuming SAP count + POS velocity + OMS sync age; circuit breaker auto-reverts all stores to binary fallback when rolling 24h High-correctness drops below 75%.
- **Payment stack:** Stripe (tokenisation); no raw card data in Meridian systems (PCI-DSS CDE isolation). Country-level local payment methods must be routed through Stripe's local payment method APIs.
- **Notification stack:** SendGrid for transactional email (reservation confirmations, cancellation alerts).
- **ML training requirement:** Offline experiment on 6 months of OMS/POS history must show ≥5% MAPE improvement before velocity signal is included in the model. Confidence score at reservation time is logged fire-and-forget (`POST /api/v1/confidence-log`) for calibration tracking.

---

## Regulatory layer

- **GDPR (EDPB, Jan 2024 guidance):** Cross-border data flows between EU member states require documented legal basis. Consent must be opt-in (not opt-out). *Architectural implication:* Confidence API must be a non-PII path — no customer identity in the `GET /confidence?sku=&storeId=` request. CDP-level personalisation (e.g., loyalty, recommendations) must enforce per-region consent gates before processing. Non-compliance fines: €10–20M+.
- **PSD2 Strong Customer Authentication (EBA, Oct 2024):** SCA exemption threshold reduced from €100 to €50. 3DS 2.0 mandatory on EU checkout. *Architectural implication:* All checkout paths must support both challenge and frictionless 3DS flows. Stripe's 3DS 2.0 integration must handle challenge redirects without breaking the reservation or cart state. Non-compliance: 5–15% transaction decline rate (Adyen estimate).
- **PCI-DSS Level 1:** *Architectural implication:* Cardholder data environment (CDE) is fully delegated to Stripe via tokenisation. Meridian systems must never touch, store, log, or transit raw card numbers or CVVs. Any system that handles a Stripe payment intent token must be scoped as a PCI-adjacent system and excluded from general-purpose logging pipelines.
- **Local payment methods (BaFin Sep 2024 / Italian regulators):** Postepay and Satispay mandatory in Italy; Giropay and Sofort mandatory in Germany. *Architectural implication:* Stripe integration must include per-country payment method routing logic. A single Stripe payment intent cannot be a country-agnostic default — country must be resolved before presenting payment options.

---

## Five implicit assumptions the brief never states

Each assumption below is something the brief implies but never explicitly confirms. If any is wrong, the downstream architecture fails in a specific, recoverable-only-with-rework way.

---

**A1 — SAP exposes an on-demand inventory query, not just a batch snapshot.**

> *Brief hints:* "Input signals: SAP inventory count + same-day POS sell-through rate" (`04-stories-acs.md`, S1 AI Eval Card). The system context brief notes "SAP S/4HANA (batch sync to OMS; 2-4h lag during peak)."

*Assumption:* The Confidence API can call SAP (or an SAP adapter) for a current count per store-SKU at request time — not just read the last batch snapshot.

*What breaks:* If SAP offers no real-time query API, the "SAP inventory count" input is the last batch value (up to 4h old). The refusal trigger "SAP sync > 4h stale" fires constantly during peak, forcing all stores into binary fallback. The confidence feature degrades to a staleness warning system, not a confidence signal. The €8M problem is not addressed.

---

**A2 — POS velocity data is available at 4-hour granularity per store, not just daily.**

> *Brief hints:* "same-day POS sell-through rate (units sold in last 4h at that store)" (`04-stories-acs.md`, S1). The context brief states: "POS: 600 stores, mix of vendors. Daily velocity aggregated to OMS; no real-time feed."

*Assumption:* A POS aggregation pipeline produces sub-day (4h window) sell-through snapshots per store-SKU, available to the ML scoring engine at inference time.

*What breaks:* If POS data is daily-only, the velocity input to the model is ~0–23h stale. The "units sold in last 4h" signal cannot be computed. Model coverage drops below the 80% floor for high-velocity stores (exactly where the phantom-stock problem is worst). S3 (velocity signal in model) cannot progress past the fallback-scoring path. The MAPE improvement experiment cannot be reproduced on live traffic.

---

**A3 — The three storefront platforms share an API gateway or BFF that the Confidence API integrates with once.**

> *Brief hints:* The PRD and SPEC describe a single `GET /api/v1/confidence?sku=&storeId=` endpoint and a single async product-page integration pattern. The storefront estate is documented as three separate platforms (Shopify Plus / custom .NET / Magento 2) with no shared gateway mentioned.

*Assumption:* A BFF or API gateway layer exists (or will be built as part of the $42M programme) that abstracts the three platforms, so the Confidence API has one integration surface, not three.

*What breaks:* Without a shared gateway, the frontend integration requires three separate implementations — different async loading mechanisms, different CSP policies, different cart state models. The 13-person-week Sprint 1 estimate assumes one frontend integration. Three-platform parallelism multiplies scope by ×2–3 and introduces divergent fallback behaviours across regions.

---

**A4 — OMS holds 6 months of labelled click-and-collect outcome data at store-SKU granularity.**

> *Brief hints:* "Offline experiment on 6 months of POS history must confirm ≥5% MAPE improvement before inclusion" (`200-PRD/06-prd.md`, S3). The PRD assumes a probabilistic model trained on Meridian's own historical data.

*Assumption:* The OMS has 6 months of C&C order outcomes labelled with cancellation cause ("item unavailable at pickup" vs. shopper-cancelled vs. other), and POS history is archived at store-SKU-day granularity with enough volume per store to train a per-store model.

*What breaks:* If OMS cancellation events are not cause-coded (or cause codes were added recently), the training set has no ground truth labels — the model cannot be trained on Meridian data. The fallback is heuristic scoring (SAP count threshold only), which the PRD explicitly rejects as insufficient. The ≥85% High-correctness calibration target cannot be validated before launch. The circuit breaker fires on day 1.

---

**A5 — Regional GM resistance is a programme governance risk, not a Sprint 1 deployment blocker.**

> *Brief hints:* "Regional GMs resist consolidation due to local language/payment nuance" (`01-Context-brief.md`). The PRD targets a 90-day success metric window but does not document which region(s) pilot first or which storefront receives the first deployment.

*Assumption:* Sprint 1 deploys the confidence signal on one pilot region (likely DE or FR, where Shopify Plus provides cleaner deployment autonomy) and does not require all 3 regional GMs to approve simultaneously before the 90-day clock starts.

*What breaks:* If each regional GM controls the CI/CD pipeline for their storefront and can veto or delay feature releases without central override, Sprint 1 cannot go live on any storefront without unanimous GM approval. The 90-day metric window cannot start. The €8M/year loss continues while programme governance is resolved. This is not an architectural fix — it requires a programme decision about deployment authority before the architecture can be delivered.
