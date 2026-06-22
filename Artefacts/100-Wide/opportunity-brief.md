---
case: Meridian
segment: EU Fashion Omnichannel (€2–4B, 8 countries, 600 stores)
date: 2026-06-18
status: draft — ROI requires Finance sign-off on Meridian CRM data before investment decision
sources: 00-playground.md, 01-Context-brief.md, 02-primary-signal.md, 03-use-cases.md, 04-canvas.md, 05-roi.csv, 07-pre-mortem.md
---

# Opportunity Brief: AI in EU Fashion Omnichannel — Meridian

**Decision this brief supports:** Go/no-go on a €250–350K pilot (12 weeks, 1–2 countries) for the #1-ranked use case.
**What this brief does NOT decide:** Problem selection, ethical go/no-go, full rollout approval, or stakeholder commitments. Those remain human-owned.

---

## 1. Situation Summary

Meridian is a €2–4B EU fashion retailer (600 stores, 8 countries, 35% online mix) losing margin to fragmented infrastructure:

| Pain Point | Validated Loss | Signal Confidence |
|------------|---------------|-------------------|
| Phantom stock (12% click-&-collect cancellation rate) | €8M/year margin + active churn to Zalando/ASOS | High — Verbatim 1–3, Zalando teardown |
| Fragmented loyalty (35% of repeat customers treated as new) | €12M/year lost upsell | High — Verbatim 5–6, Zalando +18% uplift benchmark |
| Peak-season mobile reliability (40-min Black Friday outage) | Revenue loss est. €500K–1M | Medium — Verbatim 7–8; not directly quantified |

All three pain points are **confirmed and sharpened** by primary signal (02-primary-signal.md). Competitors (Zalando, ASOS, Inditex) have solved all three; the gap is now a measurable competitive disadvantage, not just an operational inefficiency.

---

## 2. Use-Case Shortlist — Value × Feasibility Scored

Full scoring methodology and commodity check in `03-use-cases.md`.

| Rank | Use Case | Pain Point | Value (1–5) | Feasibility (1–5) | Score | Commodity Status |
|------|----------|-----------|-------------|------------------|-------|-----------------|
| **1** | **UC1.1 (Rev.) — Demand-Driven Inventory Allocation** | Phantom stock | 4 | 4 | **16** | Non-commodity (allocation + click-&-collect prioritization layer is proprietary) |
| **1** | **UC2.1 — Customer Identity Resolution** | Fragmented loyalty | 4 | 4 | **16** | Non-commodity (custom dedup of 3 legacy systems; not a CDP plug-in) |
| **3** | **UC2.2 (Rev.) — Real-time Personalized Offers** | Fragmented loyalty | 4 | 3 | **12→14** | Non-commodity (when combined with tier optimization + regional payment/language rules) |
| 4 | UC3.1 — Predictive Load Forecasting | Mobile reliability | 3 | 4 | 12 | Commodity (standard DevOps practice) — table-stakes, not differentiating |
| 5 | UC3.3 — Autonomous Perf. Monitoring | Mobile reliability | 4 | 2 | 8 | Deprioritized (autonomous actions risk cascading failures at 2/5 feasibility) |

**Recommendation for first investment:** Start with **UC1.1 (Demand-Driven Inventory Allocation)**. Highest score (tied), most contained scope (600 stores, 1 SAP integration), fastest path to a falsifiable pilot metric (phantom stock rate from 12% → ≤5% in 6 months).

**UC2.1 (Identity Resolution)** is the prerequisite for UC2.2 and should run in parallel or immediately after UC1.1. UC2.2 cannot be initiated until UC2.1 is live.

---

## 3. ROI Hypothesis — UC1.1 Demand-Driven Inventory Allocation

Full model with sensitivity analysis and source benchmarks in `05-roi.csv`.

### Three-Scenario Summary

| Scenario | Implementation Cost | Year 1 Value | Year 1 Run Cost | Year 1 Net | Payback |
|----------|-------------------|-------------|----------------|-----------|---------|
| **Pessimistic** | €1.47M | €720K | €350K | **−€1.10M** | 24–30 months |
| **Base Case** | €879K | €2.33M | €180K | **+€1.27M** | ~4.5 months |
| **Optimistic** | €425K | €4.72M | €90K | **+€4.21M** | ~1 month |

### Base-Case Value Decomposition

| Value Driver | Year 1 Value | Assumption | Confidence |
|-------------|-------------|-----------|-----------|
| Phantom stock margin saved | €900K | 12% → 5% rate; 750K orders; €100 AOV; 45% GM | Medium — order volume unverified |
| Customer churn reduction | €675K | 3% churn rate × 300K repeat customers × €750 CLV × 50% attribution | Medium — churn % unverified |
| Planner operational efficiency | €750K | 5 hrs/week saved × 50 planners × €60/hr × 50 weeks | High — Forrester 2024 benchmark |
| **Total Year 1 Value** | **€2.33M** | | |

### ⚠️ ROI Credibility Patch (from 07-pre-mortem.md)

> The €2.33M Year 1 figure is a benchmark-derived upside range, not a Meridian-validated number.
> Two assumptions require Finance sign-off before rollout approval:
> 1. **Click-&-collect order volume** — currently derived (€8M loss ÷ €10.67 AOV); must be pulled from Meridian CRM
> 2. **Repeat customer churn rate** — currently estimated (2–4%); must be validated against CRM cohort data

**Gate:** Do not present base-case ROI to steering committee until Finance has validated order volume and churn rate against actual Meridian transaction data.

---

## 4. Six-Gate Risk Read

Each gate is rated: ✅ Clear | ⚠️ Conditional | 🔴 Blocked.

### Gate 1 — Problem Gate: Is the pain real and quantified?
**Status: ✅ Clear**

- Phantom stock rate (12%) sourced from case data; validated by 3 independent customer verbatims + Zalando teardown
- Churn to named competitors (Zalando, ASOS) is explicit, not inferred
- Market context (Forrester, McKinsey, Inditex) triangulated from analyst, consulting, and competitor sources — no single source dominates
- **Residual risk:** Revenue attribution (€8M loss) is the client's own estimate; not independently validated. Low risk — order of magnitude is consistent with benchmarks.

### Gate 2 — Data Gate: Is training/operational data available and sufficient?
**Status: ⚠️ Conditional**

- **Available:** 5 years of POS + online sales history; SAP ECC current inventory (read-only sync confirmed)
- **At risk:** POS data quality (8 regional systems — Shopify Plus, custom .NET, Magento 2); manual adjustments and returns may not be recorded consistently
- **Required before pilot start:** Data quality audit on 1–2 countries' POS exports; measure completeness and consistency of SKU-level daily sales records
- **If data quality < 80% completeness:** Pilot scope must be restricted to Germany or France (highest data maturity); Italy excluded until POS data is cleaned

### Gate 3 — Solution-Fit Gate: Does AI solve the root cause, or a symptom?
**Status: ⚠️ Conditional**

*From 07-pre-mortem.md patch:*
> The root cause of phantom stock has not been diagnosed. The 12% rate could be driven by: (a) allocation/visibility — solvable by UC1.1; or (b) POS latency, inventory accuracy errors, returns not recorded, shrinkage, or store execution failures — NOT solvable by UC1.1.

- **Required before pilot start:** Root-cause diagnostic (2–3 weeks) to split phantom stock causes into allocation/visibility vs. operational errors
- **Pass threshold:** ≥40% of phantom stock attributable to allocation/visibility gap → UC1.1 is the right lever. If <40%, investment thesis changes and the problem definition must be revisited (human-owned decision)
- **Risk if skipped:** Pilot delivers model improvements but phantom stock rate does not move; pilot declared failed even if model performs correctly

### Gate 4 — ROI Gate: Does the business case hold under scrutiny?
**Status: ⚠️ Conditional**

- Base case (+€1.27M Year 1 net) is credible in structure; assumptions are cited and sensitivity-tested
- **Two assumptions are unverified** (see §3 ROI Credibility Patch): order volume and churn rate
- Pessimistic scenario is cash-flow negative in Year 1 (−€1.10M); payback stretches to 24–30 months under slow-adoption conditions
- **Required:** Finance sign-off on order volume and churn rate before rollout approval (pilot cost is de-risked at €250–350K)
- **Pilot investment (€250–350K, 12 weeks)** is justified even under pessimistic assumptions: cost is bounded, and the pilot produces the evidence needed to validate or invalidate the base case before full rollout

### Gate 5 — Delivery Gate: Can a 12-week pilot be scoped and staffed?
**Status: ✅ Clear**

- Pilot scope (1–2 countries, classical ML on tabular data, SAP read-only integration) is technically bounded
- No real-time infrastructure required in pilot phase; batch daily is sufficient for first 3 months
- SAP integration complexity is medium (4–6 weeks per Forrester 2024 ERP Integration benchmark); can be parallelized with model development
- Team requirement: 1 data engineer, 1 ML engineer, 0.5 PM, 0.5 change management — standard composition
- **Risk:** IT resource availability (SAP integration owned by IT); confirm resource commitment before pilot kick-off

### Gate 6 — Adoption Gate: Will regional GMs and planners use the recommendations?
**Status: ⚠️ Conditional**

*Key tension:* Regional GMs (e.g., Marco Italy, Junichi Japan) have historically resisted consolidation citing local language/payment nuance. Centralized allocation recommendations are a direct threat to local autonomy.

- **Canvas assumption:** ≥70% of recommendations implemented within 48 hours (Assumption 2 in 04-canvas.md)
- **Risk:** If planners trust local intuition over model output, adoption stalls and phantom stock doesn't improve
- **Mitigation:** Pilot design must include (a) regional planner involvement in model feature selection, (b) explainable recommendations ("move 20 units of SKU-12345 from Berlin because…"), (c) planner feedback loop (reject + reason captured)
- **Executive sponsorship required:** Regional GM resistance will not be resolved by the pilot team alone; CxO must mandate minimum participation in the pilot countries before launch
- **Pass threshold for rollout:** ≥70% adoption rate in pilot countries within 8 weeks of go-live

---

## 5. Recommended Next Steps (Pilot Design)

These are the team's recommended next actions. Go/no-go on the pilot is a human decision.

| Step | Owner | Timeline | Gate Unlocked |
|------|-------|----------|--------------|
| 1. Root-cause diagnostic: split phantom stock drivers (allocation vs. operational) | Retail Ops + Data team | 2–3 weeks | Gate 3 |
| 2. Data quality audit: POS completeness in 1–2 pilot countries | Data Engineering + Finance | 2 weeks | Gate 2 |
| 3. CRM validation: pull order volume and churn rate for Finance sign-off | Finance + CX | 2 weeks | Gate 4 |
| 4. Executive alignment: secure CxO sponsorship + regional GM pilot commitment | PROD/BA + Exec Sponsor | 2–3 weeks | Gate 6 |
| 5. Pilot kick-off (€250–350K, 12 weeks, 1–2 countries) | PROD + IT + Data | After Gates 2–4 pass | All |

**Stop-and-escalate if:**
- Root-cause diagnostic shows <40% of phantom stock is allocation/visibility driven (problem definition must be revisited)
- Data quality audit shows <80% POS completeness in both pilot countries (scope must be restricted or investment reconsidered)
- Finance CRM validation shows Year 1 value < €500K in pessimistic scenario (full rollout ROI may not justify €1.47M implementation cost)
- Regional GM resistance cannot be resolved with CxO sponsorship within 3 weeks (organizational readiness is a prerequisite, not a risk to manage around)

---

## 6. Human-Owned Decisions (Not Answered by This Brief)

The following are explicitly out of scope for this brief and require human judgment:

1. **Problem selection** — whether phantom stock, fragmented loyalty, or mobile reliability is the right first problem to invest in
2. **Opportunity go/no-go** — whether the overall opportunity is worth pursuing given Meridian's strategic priorities and budget cycle
3. **Ethical go/no-go** — whether personalized offer generation (UC2.2) is ethically appropriate given GDPR consent requirements and Meridian's customer relationship norms
4. **Stakeholder commitments** — regional GM alignment, IT resource allocation, Finance sign-off
5. **Final value-hypothesis framing** — the ROI numbers in §3 are a hypothesis, not a commitment; the team recommends against quoting them to steering committee before Finance validation

---

## 7. Source Quality Flags

| Claim | Source | Confidence | Action Required |
|-------|--------|-----------|----------------|
| 12% phantom stock rate | Client-provided (playground) | Medium | Validate against POS cancellation data |
| €8M/year loss | Client-provided (playground) | Medium | Validate against Finance transaction data |
| €12M/year loyalty upsell loss | Client-provided (playground) | Medium | Validate against CRM cohort analysis |
| 750K annual click-&-collect orders | Derived estimate | Low | Pull from Meridian CRM — High priority |
| 2–4% churn rate | Primary signal estimate | Low | Pull from Meridian CRM — High priority |
| Zalando +18% repeat purchase uplift | Zalando earnings call Q3 2024 | High (public, quantified) | No action required |
| €879K implementation cost (base) | Benchmark-derived | Medium | Refine after data quality audit and SAP scoping |

---

*Prepared by: consulting-sme-meridian skill (automated synthesis)*
*Inputs: 00-playground.md, 01-Context-brief.md, 02-primary-signal.md, 03-use-cases.md, 04-canvas.md, 05-roi.csv, 07-pre-mortem.md*
*Human review required before sharing with steering committee.*
