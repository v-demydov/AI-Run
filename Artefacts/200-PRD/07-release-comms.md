---
product: Meridian click-&-collect (product detail page)
feature: AI availability assistant
date: 2026-06-22
sources: 06-prd.md · 06-traceability.md
---

# Release Communications Pack: AI Availability Assistant

---

## Part 1 — Release-Scope Confirmation

### In this release

| What ships | Story | Metric |
|-----------|-------|--------|
| Velocity-adjusted confidence indicator (High / Medium / Low) on the product detail page before reservation | S1 | M1 |
| Same-day POS sell-through rate included as a model input signal | S3 | M1 |
| Warning modal intercepting reservation on a Low-confidence store, with "Choose another store" as the default action | S4 | M1 |
| Fallback to binary In-stock / Out-of-stock when model cannot score (reads from OMS cache, staleness warning if SAP >4h stale) | S7 | M1 |
| Screen-reader accessibility for confidence label and warning modal (WCAG 2.1 AA, baked into S4 delivery) | S9 | — |

### Deferred to post-launch

| What is NOT in this release | Why | Story |
|-----------------------------|-----|-------|
| Alternative store suggestions at Low confidence | Blocked — Low-signal trigger rate unknown until S1 is live and calibrated (4-week evidence gate) | S2 |
| Signal recency timestamp | Phase 2 quick win; only meaningful after S1 ships | S6 |
| Confidence logging at reservation | Phase 2; enables model calibration tracking | S11 |
| Store map with confidence indicators | Requires analytics confirmation of map usage rate | S8 |
| Home delivery fallback when all stores Low | Requires S2 live and conversion data | S5 |
| Ops monitoring dashboard | Icebox — review after 90 days of S1 data | S10 |

### Permanently out of scope

| What was cut | Reason |
|-------------|--------|
| Committed item hold (Apple model) | Incompatible with 10K+ fashion SKU depth at 600 stores |
| RFID ground-truth initiative | No Meridian infrastructure; 2–3 year timeline |

---

## Part 2 — Open Risks

**Risk 1 — Model calibration misses the High-correctness target at launch**
- Specific failure: the velocity-adjusted model does not achieve ≥85% High-correctness on production data; the circuit breaker fires; the feature auto-reverts to binary fallback for all users at launch.
- Owner: Data Science Lead
- Mitigation: run 4-week offline calibration experiment on 6 months of historical POS data before production deployment; confirm ≥5% MAPE improvement from velocity signal. If offline experiment fails, ship S1 with SAP-only model (no velocity signal; exclude S3 from Sprint 1); velocity signal added in Sprint 2 once data quality is confirmed.

**Risk 2 — SAP integration latency exceeds async budget**
- Specific failure: OMS sync latency causes confidence score to miss the p95 ≤ 800ms ceiling; product page blocks on the confidence API; conversion rate drops before M2 counter-metric can catch it.
- Owner: Backend / IT Integration Lead
- Mitigation: async load confirmed in S1 AC (confidence label renders after page; never blocks); OMS snapshot cache TTL ≤ 30 min; if SAP API p95 exceeds 2s in staging, switch to fallback path (S7) for the affected stores only and investigate SAP bottleneck before full rollout.

**Risk 3 — Regional GMs request store-level feature suppression**
- Specific failure: store GMs in Italy or Germany flag that "Low confidence" labels are damaging their in-store conversion metrics and request the feature be disabled for their stores before data supports this.
- Owner: Retail Ops / Product Lead
- Mitigation: executive sponsorship confirmed before launch; Low-confidence signal rate and cancellation delta shared with GMs weekly from day one; pilot in 1–2 countries with transparent reporting so GMs see the cancellation reduction alongside the conversion counter-metric before full rollout.

---

## Part 3 — Stakeholder Notifications

### For Delivery Leads (scope · risks · timeline)

**Subject:** AI Availability Assistant — Sprint 1 release scope and risks confirmed

**Scope:** Sprint 1 ships five stories as a package: confidence indicator (S1), POS velocity signal (S3), Low-confidence warning modal (S4), fallback safety (S7), and accessibility (S9). Six stories are deferred post-launch (S2, S5, S6, S8, S11) and one is iced (S10). Committed item hold and RFID are permanently out of scope.

**Timeline:** Sprint 1 is approximately 13 person-weeks. The S3 velocity signal is conditional on a 4-week offline calibration experiment passing; if it fails, S1 ships with a SAP-only model and S3 moves to Sprint 2.

**Three risks to watch:**
1. Model calibration: circuit breaker may revert feature to binary fallback at launch if High-correctness < 75% rolling 24h (Data Science Lead owns)
2. SAP integration latency: async load mitigates page-blocking risk, but OMS p95 must be confirmed in staging before go-live (IT Integration Lead owns)
3. Regional GM resistance: exec sponsorship required before launch to prevent store-level suppression requests (Retail Ops Lead owns)

**Action needed:** Confirm Data Science Lead availability for 4-week offline calibration before sprint kick-off. Confirm IT integration resource for SAP/OMS connector work (4–6 weeks per Forrester benchmark). Confirm executive sponsor.

---

### For Business / External Stakeholders (value · timeline · plain language)

**Subject:** Meridian click & collect — fewer wasted trips, starting [launch date]

We're launching a feature that tells click-and-collect shoppers how confident we are that their item will actually be on the shelf when they arrive — before they make the trip.

Today, 7 in every 100 click-and-collect orders end in a cancellation at the pickup counter because the website's stock count doesn't always reflect what's physically in-store. That costs customers a wasted journey and costs us their trust. The AI availability assistant uses real-time sales data and inventory signals to show shoppers a High, Medium, or Low confidence level on the product page. Shoppers who see Low confidence get a clear prompt to choose a different store or reconsider — so they're never surprised at the counter.

**What changes for customers:**
- See a confidence level before reserving click-and-collect
- Get a clear warning (and an alternative) if their nearest store shows Low confidence
- Always see a clear stock status even when the live estimate is temporarily unavailable

**What stays the same:** The reservation flow, checkout, and home delivery experience are unchanged.

**Target:** We expect click-and-collect cancellations at pickup to fall from 7% to below 4% within 90 days of launch. We will measure this weekly.

**Timeline:** [Sprint 1 launch date — to be confirmed at sprint kick-off.]

---

## Part 4 — "What's New" Release Note

*Each bullet verified against 06-traceability.md. Any claim not traceable to a shipped story has been cut.*

- **Confidence signal before you reserve.** The product page now shows whether an item is High, Medium, or Low confidence for click-and-collect at your nearest store — calculated from real-time sales data, not just a stock count snapshot. *(traces to S1 → M1)*

- **Powered by today's sell-through rate.** The confidence signal accounts for how fast the item is selling at that specific store today, so a "High" during a busy Saturday flash sale is still trustworthy. *(traces to S3 → M1)*

- **Clear warning before you commit to a Low-confidence store.** If you tap Reserve at a store with Low confidence, a prompt appears so you can choose to look for a better store or proceed knowingly — before the trip, not after. *(traces to S4 → M1)*

- **Always a clear answer, even when live data is unavailable.** If the confidence estimate can't be generated (for example, if stock data is temporarily out of date), you'll see a standard In stock / Out of stock status with a clear "data may be outdated" notice — never a misleading live estimate. *(traces to S7 → M1)*

*Cut (not traceable to a shipped story): "See alternative stores with confirmed stock" — S2 is deferred pending calibration data. Not included in this release.*

---

## Part 5 — Spec Update on Ship

Once Sprint 1 ships and 90-day M1 / M2 data is available: **update `01-vision.md` success metric baseline** — replace the 7% cancellation baseline with the observed post-launch rate, and either confirm ≤4% target was met (close the vision) or revise the target and reopen the evidence gate for S2 (alternative stores).
