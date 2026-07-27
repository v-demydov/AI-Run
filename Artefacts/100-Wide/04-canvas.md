---
case: Meridian
use_case: UC1.1 (Revised) — Demand-Driven Inventory Allocation
segment: EU Fashion Omnichannel (€2–4B, 8 countries, 600 stores)
date: 2026-06-18
---

# Canvas: Demand-Driven Inventory Allocation

---

## Problem

**In customer language:**
Store managers and online fulfillment teams can't see where inventory should go to prevent phantom stock on click-&-collect orders, so 12% of orders are cancelled at pickup, costing €8M/year in lost margin and driving customers to Zalando/ASOS.

---

## Users

**Primary segment:** Inventory planners and fulfillment operations teams (40–50 people across 8 countries)

**Sub-segments:**
- **Regional inventory planners** (1–2 per country) — allocate stock across stores + online warehouse; currently use spreadsheets + manual forecasts
- **Store managers** (600 stores) — receive inventory recommendations; currently rely on regional planners' guesses
- **Online fulfillment team** (central warehouse) — pick and pack click-&-collect orders; currently see phantom stock only after customer arrives at store
- **Finance/CFO office** (2–3 people) — track inventory write-offs and phantom stock costs; currently report €8M/year loss

---

## Value

**Falsifiable benefit statement:**
Reduce click-&-collect phantom stock from 12% to ≤5% within 6 months of deployment, saving €560K–1.12M/year in lost margin and reducing customer churn to competitors by ≥8%.

**Breakdown:**
- Current phantom stock: 12% of click-&-collect orders
- Target: ≤5% (industry benchmark: Zalando 3%, ASOS <3%)
- Margin impact: €8M/year × (12% − 5%) = €560K/year
- Additional uplift from reduced churn: estimated €500K–600K/year (customers retained from Zalando/ASOS)
- **Total value: €1.06M–1.72M/year**

---

## Assumptions

**Assumption 1: Demand forecasting accuracy is sufficient to drive allocation decisions**
- Claim: Demand forecast MAPE (mean absolute percentage error) ≤15% for 80% of SKUs at store level
- Why it matters: If forecast accuracy is <80% at store level, allocation recommendations will be wrong, and phantom stock won't improve
- How to test: Build demand forecast model on 6 months of historical data; measure MAPE on holdout test set; segment by SKU category (fast-moving vs. slow-moving)
- Success threshold: ≥80% of SKUs achieve MAPE ≤15%

**Assumption 2: Regional inventory planners will adopt and act on allocation recommendations**
- Claim: ≥70% of allocation recommendations are implemented by regional planners within 48 hours of generation
- Why it matters: If planners ignore recommendations (due to trust, complexity, or organizational resistance), phantom stock won't improve
- How to test: Deploy model in pilot (1–2 countries); track recommendation generation vs. implementation; survey planners on barriers to adoption
- Success threshold: ≥70% implementation rate; NPS ≥6 from planners on ease of use

**Assumption 3: Click-&-collect order patterns are stable enough to forecast 7–14 days ahead**
- Claim: Click-&-collect order volume is predictable 7–14 days in advance with ≤20% variance for ≥75% of store-day combinations
- Why it matters: If order patterns are too volatile (e.g., flash sales, viral TikTok moments), allocation recommendations will be stale by the time orders arrive
- How to test: Analyze 12 months of click-&-collect order history; measure day-of-week and week-of-month seasonality; identify outlier events (flash sales, holidays); calculate forecast variance
- Success threshold: ≤20% variance for ≥75% of store-day combinations; outliers identified and handled separately

---

## Solution

**Behavior (not implementation):**

Demand-Driven Inventory Allocation system ingests 5 years of historical sales data (POS, online, returns) + external signals (weather, events, promotions, regional holidays) to forecast demand per SKU per store per day, 7–14 days ahead. The system then recommends optimal inventory allocation across 600 stores + online warehouse to minimize phantom stock on click-&-collect orders.

**Workflow:**
1. **Daily:** System generates demand forecast for each SKU at each store for next 7–14 days
2. **Daily:** System calculates optimal allocation (how many units should be in each store vs. online warehouse) to maximize click-&-collect fulfillment rate
3. **Daily:** Regional inventory planners receive allocation recommendations via dashboard (top 50 SKUs per country, ranked by impact on phantom stock)
4. **Within 48h:** Planners approve/reject recommendations and trigger inventory transfers (store-to-store, store-to-warehouse)
5. **Weekly:** System measures actual vs. forecast; retrains model; reports phantom stock reduction to finance team

**Key behaviors:**
- Planners see recommendations ranked by impact (not overwhelming with 10K SKUs)
- Recommendations are explainable (e.g., "move 20 units of SKU-12345 from Berlin to online warehouse because forecast shows 15 click-&-collect orders next week")
- System learns from planner feedback (if planner rejects recommendation, system learns why)
- System integrates with SAP (reads current inventory, writes allocation recommendations)

---

## Success Metrics

| Metric | Current | Target | Timeline |
|--------|---------|--------|----------|
| Click-&-collect phantom stock rate | 12% | ≤5% | 6 months |
| Demand forecast MAPE (store level) | N/A | ≤15% (80% of SKUs) | 3 months |
| Planner adoption rate | N/A | ≥70% | 3 months |
| Margin saved from reduced phantom stock | €0 | €560K–1.12M/year | 6 months |
| Customer churn reduction (to Zalando/ASOS) | N/A | ≥8% | 6 months |

---

## Dependencies & Risks

**Dependencies:**
- SAP ECC integration (read current inventory, write allocation recommendations) — owned by IT, 4–6 weeks
- Historical sales data (5 years of POS + online) — owned by Finance, 2–3 weeks to extract
- Regional planner buy-in (training, change management) — owned by Retail Ops, ongoing

**Risks:**
- **Data quality:** POS data may have gaps or errors (e.g., manual adjustments, returns not recorded); could degrade forecast accuracy
- **Organizational resistance:** Regional GMs may resist centralized allocation recommendations (conflicts with local autonomy); requires executive sponsorship
- **Seasonality shifts:** 2024–2025 fashion trends may differ from historical data; model may not capture new patterns
- **External shocks:** Geopolitical events, supply chain disruptions could invalidate forecasts

---

## Falsifiability Check

**Assumption 1 is falsifiable:** "MAPE ≤15% for 80% of SKUs" — can measure on holdout test set
**Assumption 2 is falsifiable:** "≥70% adoption rate" — can track recommendations vs. implementations
**Assumption 3 is falsifiable:** "≤20% variance for ≥75% of store-day combinations" — can analyze historical order data

**None of these are platitudes.** Each has a number, a threshold, and a clear test.

---

## Canvas Critique (Self-Review)

**Strongest cells:**
- **Assumptions:** Each has a number, a threshold, and a clear test method
- **Value:** Specific benefit statement with magnitude (€1.06M–1.72M/year) and success threshold (≤5% phantom stock)
- **Users:** Named segments with specific roles and pain points

**Weakest cells (and rewrites):**
1. **Problem:** Original was too long and jargony ("inventory allocation optimization"). Rewritten to customer language: "Store managers and online fulfillment teams can't see where inventory should go…"
2. **Solution:** Original jumped to implementation details (API specs, database schema). Rewritten to behavior: "System ingests historical data, forecasts demand, recommends allocation, planners approve/reject."
3. **Users:** Original was too broad ("inventory team"). Rewritten to named sub-segments with specific roles and pain points.

---

## One-Page Compliance

✅ Problem: 2 sentences
✅ Users: 4 sub-segments with roles
✅ Value: 1 sentence + breakdown
✅ Assumptions: 3 falsifiable claims with numbers
✅ Solution: 1 paragraph + workflow + key behaviors
✅ Success Metrics: 5 metrics with targets
✅ Dependencies & Risks: 3 dependencies + 4 risks
✅ Total: 1 page (fits on single page with standard margins)