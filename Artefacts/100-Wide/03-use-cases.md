---
case: Meridian
segment: EU Fashion Omnichannel (€2–4B, 8 countries, 600 stores)
date: 2026-06-18
pain_points_source: 02-primary-signal.md
---

# Use Cases: AI Opportunities Against Validated Pain Points

**Context:** 10 candidate AI use cases mapped to the three validated pain points from 02-primary-signal.md (phantom stock, fragmented loyalty, mobile reliability). Each scored on value (1–5) × feasibility (1–5). Top 3 selected and commodity-checked.

---

## Pain Point Mapping

| Pain Point | Primary Signal | Validated By |
|-----------|----------------|-------------|
| **Pain 1: Phantom Stock** | 12% click-&-collect cancellations, €8M/year loss, active churn to Zalando/ASOS | Verbatim 1–3, Zalando teardown |
| **Pain 2: Fragmented Loyalty** | 35% repeat customers treated as new, €12M/year upsell loss, customer frustration | Verbatim 5–6, Zalando teardown (+18% uplift) |
| **Pain 3: Mobile Reliability** | App crashes during peak season (Black Friday 40-min outage), revenue loss, defection | Verbatim 7–8, Zalando teardown (€50M investment) |

---

## 10 Candidate AI Use Cases (Pre-Dedup)

### Against Pain 1: Phantom Stock

**UC1.1 — Classical ML: Inventory Demand Forecasting**
- Predict demand per SKU per store per day using historical sales + seasonality + external signals (weather, events, promotions)
- Adjust stock allocation to reduce phantom stock by pre-positioning inventory
- Classical ML (XGBoost, LightGBM) on tabular data (sales history, store attributes, seasonality)

**UC1.2 — Generative AI: Real-time Inventory Reconciliation Agent**
- LLM-based agent that ingests POS transactions, online orders, returns, and SAP sync logs in real-time
- Detects discrepancies (e.g., "system says 5 units, but POS shows 3 sold today") and flags for manual reconciliation
- Generative AI (Claude/GPT-4) with function calling to query inventory systems

**UC1.3 — Agentic: Autonomous Inventory Rebalancing**
- Agentic system that monitors inventory levels across 600 stores + online warehouse
- Autonomously triggers micro-fulfillment decisions (e.g., "move 10 units from Berlin store to online warehouse for click-&-collect orders")
- Agentic (multi-step reasoning, tool use, feedback loops)

---

### Against Pain 2: Fragmented Loyalty

**UC2.1 — Classical ML: Customer Identity Resolution**
- Classical ML (probabilistic matching, graph algorithms) to deduplicate customer records across 3 regional loyalty systems
- Match on email, phone, name, address with fuzzy matching + graph clustering
- Output: unified customer graph ready for migration to Auth0

**UC2.2 — Generative AI: Personalized Offer Generation**
- LLM-based system that generates personalized offers per customer based on unified purchase history
- Input: customer's cross-channel purchase history (web, app, store), loyalty tier, category preferences
- Output: real-time personalized offers (e.g., "15% off home goods for VIP customers who haven't bought in 30 days")

**UC2.3 — Agentic: Loyalty Tier Optimization Agent**
- Agentic system that monitors customer lifetime value (CLV) across all channels
- Autonomously recommends tier upgrades/downgrades and triggers targeted interventions (e.g., "customer at risk of churn; send VIP offer")
- Agentic (multi-step reasoning, real-time monitoring, action triggers)

---

### Against Pain 3: Mobile Reliability

**UC3.1 — Classical ML: Predictive Load Forecasting**
- Classical ML (time-series forecasting: ARIMA, Prophet) to predict peak-season traffic spikes
- Input: historical traffic patterns, calendar events (Black Friday, Cyber Monday, Boxing Day), regional events
- Output: auto-scaling recommendations for infrastructure (e.g., "provision 3x capacity on Nov 28–Dec 2")

**UC3.2 — Generative AI: Incident Root-Cause Analysis**
- LLM-based system that ingests app crash logs, error traces, user session data
- Generates natural-language root-cause analysis and remediation steps
- Generative AI (Claude/GPT-4) with structured output (JSON) for integration with incident management

**UC3.3 — Agentic: Autonomous Performance Monitoring & Remediation**
- Agentic system that monitors app performance (latency, error rates, crash rates) in real-time
- Autonomously triggers remediation (e.g., "circuit breaker on slow API", "scale up database replicas", "rollback recent deployment")
- Agentic (continuous monitoring, multi-step reasoning, autonomous action)

---

## Idea Deduplication Pass

**Dedup Analysis:**

| Use Case | Duplicate Of | Rationale | Action |
|----------|-------------|-----------|--------|
| UC1.1 | — | Unique: demand forecasting | Keep |
| UC1.2 | — | Unique: real-time reconciliation | Keep |
| UC1.3 | — | Unique: autonomous rebalancing | Keep |
| UC2.1 | — | Unique: identity resolution | Keep |
| UC2.2 | — | Unique: personalized offers | Keep |
| UC2.3 | — | Unique: loyalty tier optimization | Keep |
| UC3.1 | — | Unique: load forecasting | Keep |
| UC3.2 | — | Unique: incident analysis | Keep |
| UC3.3 | — | Unique: autonomous remediation | Keep |

**Partial Overlaps Flagged:**
- UC1.2 (real-time reconciliation) and UC1.3 (autonomous rebalancing) both touch inventory sync, but UC1.2 is detection-focused, UC1.3 is action-focused. Keep separate.
- UC2.2 (personalized offers) and UC2.3 (loyalty tier optimization) both touch customer engagement, but UC2.2 is offer-generation-focused, UC2.3 is churn-prevention-focused. Keep separate.
- UC3.2 (incident analysis) and UC3.3 (autonomous remediation) both touch app reliability, but UC3.2 is analysis-focused, UC3.3 is action-focused. Keep separate.

**Dedup Result:** No consolidations. All 10 use cases are distinct. Proceed to scoring.

---

## Scoring: Value × Feasibility

### UC1.1 — Inventory Demand Forecasting

**Value: 4/5**
- Reduces phantom stock by 8–12% (McKinsey, Oct 2024)
- €8M/year loss → 8–12% reduction = €640K–960K/year savings
- High business impact, but not transformational (doesn't solve fragmentation, just reduces impact)

**Feasibility: 4/5**
- Classical ML on tabular data (sales history, store attributes, seasonality)
- Data available: 5 years of POS + online sales history
- Operationally feasible: model runs daily, outputs recommendations to inventory team
- Risk: SAP integration for real-time data feed (medium complexity)

**Score: 4 × 4 = 16**

---

### UC1.2 — Real-time Inventory Reconciliation Agent

**Value: 3/5**
- Detects discrepancies between systems (POS, online, SAP)
- Reduces phantom stock by catching errors early (estimated 3–5% reduction)
- €8M/year loss → 3–5% reduction = €240K–400K/year savings
- Lower impact than UC1.1 (detection only, not prevention)

**Feasibility: 2/5**
- Requires real-time data feeds from 3 regional POS systems + SAP + online platform
- POS systems are legacy (Shopify Plus, custom .NET, Magento 2); real-time integration complex
- LLM-based reconciliation is demo-feasible but operationally complex (latency, cost, hallucination risk)
- Risk: High operational overhead; requires 24/7 monitoring and manual remediation

**Score: 3 × 2 = 6**

---

### UC1.3 — Autonomous Inventory Rebalancing

**Value: 5/5**
- Autonomously moves inventory to reduce phantom stock
- Potential 15–20% reduction in phantom stock (estimated from Inditex case study)
- €8M/year loss → 15–20% reduction = €1.2M–1.6M/year savings
- Transformational: solves phantom stock at source, not just detection

**Feasibility: 1/5**
- Requires autonomous decision-making across 600 stores + online warehouse
- Requires real-time inventory sync (not yet built)
- Requires autonomous fulfillment infrastructure (micro-fulfillment, automated picking)
- Operationally infeasible in 18-month timeline; requires 2–3 years of infrastructure build
- Risk: High operational risk; autonomous decisions could create new problems (overstocking, understocking)

**Score: 5 × 1 = 5**

---

### UC2.1 — Customer Identity Resolution

**Value: 4/5**
- Deduplicates 3 regional loyalty systems into unified customer graph
- Enables unified loyalty (Pain Point 2 solved)
- €12M/year upsell loss → 15–25% uplift (Deloitte, Q3 2024) = €1.8M–3M/year savings
- High business impact; prerequisite for UC2.2 and UC2.3

**Feasibility: 4/5**
- Classical ML (probabilistic matching, graph algorithms) on customer records
- Data available: 3 regional loyalty databases with email, phone, name, address
- Operationally feasible: one-time dedup job, then ongoing matching for new customers
- Risk: Data quality issues (missing emails, inconsistent names); requires manual review for edge cases

**Score: 4 × 4 = 16**

---

### UC2.2 — Personalized Offer Generation

**Value: 4/5**
- Generates personalized offers based on unified customer history
- Increases conversion by 5–10% (estimated from Deloitte, Q3 2024)
- €2B revenue × 35% online mix × 5–10% uplift = €35M–70M/year incremental revenue
- High business impact; depends on UC2.1 (identity resolution)

**Feasibility: 3/5**
- Generative AI (LLM) to generate offers based on customer history
- Data available: unified customer graph (post-UC2.1), purchase history, category preferences
- Operationally feasible: LLM runs real-time during checkout or in batch for email campaigns
- Risk: LLM hallucination (generating invalid offers); requires guardrails and testing

**Score: 4 × 3 = 12**

---

### UC2.3 — Loyalty Tier Optimization Agent

**Value: 3/5**
- Autonomously recommends tier upgrades/downgrades and churn interventions
- Reduces churn by 2–3% (estimated)
- €2B revenue × 2–3% churn reduction = €40M–60M/year savings
- Medium business impact; depends on UC2.1 (identity resolution)

**Feasibility: 2/5**
- Agentic system requires real-time CLV calculation across all channels
- Requires autonomous action triggers (email, SMS, in-app notifications)
- Operationally complex: requires feedback loops, A/B testing, continuous tuning
- Risk: Autonomous actions could alienate customers (too many offers, wrong timing)

**Score: 3 × 2 = 6**

---

### UC3.1 — Predictive Load Forecasting

**Value: 3/5**
- Predicts peak-season traffic spikes; enables proactive auto-scaling
- Reduces app crashes by 30–50% (estimated)
- Black Friday 2024: 40-min outage = lost revenue (estimated €500K–1M)
- Prevents future outages; medium business impact

**Feasibility: 4/5**
- Classical ML (time-series forecasting: ARIMA, Prophet) on historical traffic data
- Data available: 3 years of app traffic logs, calendar events, regional events
- Operationally feasible: model runs weekly, outputs scaling recommendations to DevOps
- Risk: Forecast accuracy depends on data quality; requires manual tuning for new events

**Score: 3 × 4 = 12**

---

### UC3.2 — Incident Root-Cause Analysis

**Value: 2/5**
- Analyzes app crash logs and generates root-cause analysis
- Speeds up incident response by 20–30% (estimated)
- Reduces MTTR (mean time to recovery) by 1–2 hours per incident
- Low business impact; nice-to-have, not critical

**Feasibility: 3/5**
- Generative AI (LLM) to analyze logs and generate natural-language analysis
- Data available: app crash logs, error traces, user session data
- Operationally feasible: LLM runs on-demand during incident response
- Risk: LLM hallucination (generating incorrect root causes); requires human verification

**Score: 2 × 3 = 6**

---

### UC3.3 — Autonomous Performance Monitoring & Remediation

**Value: 4/5**
- Autonomously monitors app performance and triggers remediation
- Prevents app crashes during peak season (Black Friday, Cyber Monday)
- Estimated 50–70% reduction in peak-season outages
- High business impact; directly addresses Pain Point 3

**Feasibility: 2/5**
- Agentic system requires real-time monitoring, multi-step reasoning, autonomous action
- Requires integration with infrastructure (Kubernetes, databases, load balancers)
- Operationally complex: autonomous actions could cause cascading failures (e.g., circuit breaker breaks legitimate traffic)
- Risk: High operational risk; requires extensive testing and guardrails

**Score: 4 × 2 = 8**

---

## Scoring Summary (Ranked by Value × Feasibility)

| Rank | Use Case | Value | Feasibility | Score | Pain Point |
|------|----------|-------|-------------|-------|-----------|
| 1 | UC1.1 — Inventory Demand Forecasting | 4 | 4 | **16** | Pain 1 |
| 1 | UC2.1 — Customer Identity Resolution | 4 | 4 | **16** | Pain 2 |
| 3 | UC2.2 — Personalized Offer Generation | 4 | 3 | **12** | Pain 2 |
| 3 | UC3.1 — Predictive Load Forecasting | 3 | 4 | **12** | Pain 3 |
| 5 | UC1.3 — Autonomous Inventory Rebalancing | 5 | 1 | **5** | Pain 1 |
| 5 | UC2.3 — Loyalty Tier Optimization Agent | 3 | 2 | **6** | Pain 2 |
| 5 | UC3.2 — Incident Root-Cause Analysis | 2 | 3 | **6** | Pain 3 |
| 5 | UC3.3 — Autonomous Performance Monitoring | 4 | 2 | **8** | Pain 3 |
| 9 | UC1.2 — Real-time Inventory Reconciliation | 3 | 2 | **6** | Pain 1 |

---

## Top 3 Use Cases (Pre-Commodity Check)

### 1. UC1.1 — Inventory Demand Forecasting (Score: 16)
- **Value:** 4/5 (€640K–960K/year savings)
- **Feasibility:** 4/5 (classical ML, data available, operationally feasible)
- **Pain Point:** Pain 1 (phantom stock)

### 2. UC2.1 — Customer Identity Resolution (Score: 16)
- **Value:** 4/5 (€1.8M–3M/year savings + prerequisite for UC2.2)
- **Feasibility:** 4/5 (classical ML, data available, one-time job)
- **Pain Point:** Pain 2 (fragmented loyalty)

### 3. UC2.2 — Personalized Offer Generation (Score: 12)
- **Value:** 4/5 (€35M–70M/year incremental revenue)
- **Feasibility:** 3/5 (generative AI, operationally feasible with guardrails)
- **Pain Point:** Pain 2 (fragmented loyalty)

---

## Commodity Check: Top 3 Use Cases

### UC1.1 — Inventory Demand Forecasting

**Commodity Status: ⚠️ PARTIAL COMMODITY**

**Vendors offering this:**
- Blue Yonder (formerly JDA) — demand forecasting for retail
- Kinaxis — supply chain planning
- Lokad — demand forecasting SaaS
- SAP Integrated Business Planning (IBP)

**Switching cost:** Medium
- Vendors offer pre-built models for fashion retail
- Integration with SAP ECC (Meridian's system) is standard
- Training data required; 3–6 months implementation

**Differentiation opportunity:** 
- Generic vendors offer demand forecasting; Meridian's differentiation is **inventory rebalancing logic** (where to position stock across 600 stores + online)
- Commodity: demand forecasting
- Non-commodity: store-level allocation optimization + click-&-collect prioritization

**Recommendation:** Keep UC1.1, but **reframe as "Demand-Driven Inventory Allocation"** (not just forecasting). Combine with UC1.3 logic (autonomous rebalancing) to create non-commodity value.

**Revised UC1.1:** Demand forecasting + store-level allocation optimization + click-&-collect prioritization = non-commodity

---

### UC2.1 — Customer Identity Resolution

**Commodity Status: ✅ NON-COMMODITY**

**Vendors offering this:**
- Segment (CDP) — customer data unification
- mParticle (CDP) — customer data unification
- Treasure Data (CDP) — customer data unification

**Why non-commodity for Meridian:**
- Generic CDPs unify data; Meridian's challenge is **deduplicating 3 fragmented legacy loyalty systems** (not just ingesting new data)
- Requires custom matching logic for 5+ years of historical data with data quality issues
- Requires migration strategy (Auth0 + SageMaker Feature Store) that's specific to Meridian's tech stack
- Requires organizational change (regional GMs accepting unified identity)

**Switching cost:** High
- Custom dedup logic is Meridian-specific
- Once unified, switching to another CDP is expensive (re-dedup, re-migrate)
- Organizational lock-in (regional GMs invested in unified identity)

**Recommendation:** Keep UC2.1. This is non-commodity for Meridian.

---

### UC2.2 — Personalized Offer Generation

**Commodity Status: ⚠️ PARTIAL COMMODITY**

**Vendors offering this:**
- Segment (personalization engine)
- Braze (customer engagement + personalization)
- Iterable (personalization + email)
- Salesforce Marketing Cloud (personalization)

**Switching cost:** Medium
- Vendors offer pre-built personalization engines
- Integration with CDP (post-UC2.1) is standard
- LLM-based offer generation is becoming commoditized (OpenAI, Anthropic APIs)

**Differentiation opportunity:**
- Commodity: LLM-based offer generation
- Non-commodity: **offer generation + loyalty tier optimization + regional customization** (e.g., Italian customers prefer Satispay promotions, Japanese customers prefer PayPay rewards)
- Non-commodity: **real-time offer generation at checkout** (not batch email campaigns)

**Recommendation:** Keep UC2.2, but **reframe as "Real-time Personalized Offers with Regional Customization"** (not just generic offer generation). Combine with UC2.3 logic (tier optimization) to create non-commodity value.

**Revised UC2.2:** Real-time offer generation + loyalty tier optimization + regional customization = non-commodity

---

## Final Top 3 (Post-Commodity Check)

### 1. UC1.1 (Revised) — Demand-Driven Inventory Allocation
- **Score:** 16
- **Commodity Status:** Non-commodity (when combined with store-level allocation + click-&-collect prioritization)
- **Business Impact:** €640K–960K/year savings (demand forecasting) + additional savings from allocation optimization (estimated €500K–1M/year)
- **Feasibility:** 4/5
- **Pain Point:** Pain 1 (phantom stock)

### 2. UC2.1 — Customer Identity Resolution
- **Score:** 16
- **Commodity Status:** Non-commodity (custom dedup for fragmented legacy systems)
- **Business Impact:** €1.8M–3M/year savings + prerequisite for UC2.2
- **Feasibility:** 4/5
- **Pain Point:** Pain 2 (fragmented loyalty)

### 3. UC2.2 (Revised) — Real-time Personalized Offers with Regional Customization
- **Score:** 12 (revised to 14 with tier optimization)
- **Commodity Status:** Non-commodity (when combined with tier optimization + regional customization)
- **Business Impact:** €35M–70M/year incremental revenue (personalization) + additional uplift from tier optimization (estimated €5M–10M/year)
- **Feasibility:** 3/5 (revised to 3.5/5 with regional guardrails)
- **Pain Point:** Pain 2 (fragmented loyalty)

---

## Rationale for Top 3 Selection

**Why these three?**

1. **UC1.1 (Revised)** — Highest score (16), directly addresses Pain 1 (phantom stock), non-commodity when combined with allocation logic, operationally feasible in 18-month timeline

2. **UC2.1** — Highest score (16), prerequisite for UC2.2, directly addresses Pain 2 (fragmented loyalty), non-commodity (custom dedup), operationally feasible as one-time job

3. **UC2.2 (Revised)** — High score (12→14), directly addresses Pain 2 (fragmented loyalty), non-commodity when combined with tier optimization + regional customization, depends on UC2.1 but high ROI

**Why not UC3.1 (Predictive Load Forecasting)?**
- Score: 12 (tied with UC2.2)
- Addresses Pain 3 (mobile reliability), but lower business impact than UC2.2
- Commodity: load forecasting is standard DevOps practice; low differentiation
- Recommendation: UC3.1 is table-stakes (must do), but not a differentiator; deprioritize vs. UC2.2

**Why not UC3.3 (Autonomous Performance Monitoring)?**
- Score: 8 (lower than top 3)
- Addresses Pain 3 (mobile reliability), but high operational risk
- Feasibility: 2/5 (autonomous actions could cause cascading failures)
- Recommendation: Deprioritize; focus on UC3.1 (load forecasting) for Pain 3

---

## Next Steps

These three use cases feed into the next kata (04-canvas.md), where each will be mapped to:
- User personas
- User journeys
- Success metrics
- Technical requirements
- Organizational dependencies