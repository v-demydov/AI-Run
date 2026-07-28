---
kata: 7.W (pipeline series)
date: 2026-07-28
pipeline: Nordstar Customer 360 — Bronze → Silver → Gold
---

# Lineage Diagram — Nordstar Retail Pipeline

## Data flow

```
[Source]                    [Bronze]                    [Silver]
Nordstar POS system    →    bronze/                →    silver/
transactions export         transactions_raw.csv         transactions_clean.parquet
(seed=42, 500 rows)         (500 rows, as-is)            (459 rows)
                                                         Row math: 500 − 25 (null amount)
                                                                       − 16 (dup extras) = 459
                                 ↓                            ↓
                            [Gold Table 1]              [Gold Table 2]
                            gold/                        gold/
                            daily_sales_by_category      returns_rate.parquet
                            .parquet                     (260 rows)
                            (351 rows)                   Grain: 1 row / order_date
                            Grain: 1 row /
                            (order_date, region,
                             product_category)
                                 ↓                            ↓
                         [Consumer 1]                 [Consumer 2]
                         Streamlit dashboard           Regional managers
                         kata-workspace/app.py         weekly meeting report
                         (Sales Performance            (Returns Rate Over Time
                          Dashboard)                    chart)
```

## Gold table contracts

### daily_sales_by_category

| Field | Type | Formula / source |
|-------|------|-----------------|
| order_date | DATE | silver.order_date (standardised from 3 formats) |
| region | VARCHAR | silver.region |
| product_category | VARCHAR | silver.product_category |
| total_revenue | DOUBLE | SUM(amount) WHERE status='completed' AND amount > 0 |
| order_count | INTEGER | COUNT(DISTINCT order_id) WHERE status='completed' AND amount > 0 |

Grain: one row per (order_date, region, product_category) with at least one completed order.
Consumer: Streamlit app → "Revenue by Region & Category" grouped bar chart.
DQ gate: grain check (total = unique_combos), total_revenue > 0, order_count > 0.

### returns_rate

| Field | Type | Formula / source |
|-------|------|-----------------|
| order_date | DATE | silver.order_date |
| total_orders | INTEGER | COUNT(*) WHERE status IN ('completed', 'returned') |
| returned_orders | INTEGER | COUNT(*) WHERE status = 'returned' |
| returns_rate_pct | DOUBLE | COALESCE(returned_orders / NULLIF(total_orders, 0) × 100, 0.0) |

Grain: one row per order_date.
Denominator: completed + returned (pending/in-progress excluded — not yet finalised).
Consumer: Streamlit app → "Returns Rate Over Time" line chart; VP Operations weekly review.
DQ gate: pct in [0, 100], returned_orders ≤ total_orders, 0 NULL rows.

## Human-owned decisions recorded here

| Decision | Owner | Date | Resolution |
|----------|-------|------|------------|
| customer_id is integer (non-PII) | Data Governance | 2026-07-28 | Confirmed: synthetic integer key, no email/name/ID in scope |
| "returns rate" denominator = completed + returned (exclude pending) | Data Product Owner | 2026-07-28 | Confirmed: pending orders are not finalised outcomes; denominator is actionable completions only |
| DQ blocker-vs-warning: negative revenue on completed orders | Data Product Owner | 2026-07-28 | Blocker — fixed at gold layer (filter completed AND amount > 0); 5 source rows excluded and logged |

## Sources

- **Upstream**: Nordstar POS export → `kata-workspace/bronze/transactions_raw.csv`
- **Schema reference**: `Artefacts/700-wide/bronze-profile.md`
- **Cleaning rules**: K 7.W.2 silver cell in `kata-workspace/pipeline-kata.ipynb`
- **Metric definitions**: K 7.W.3 gold cell + `Artefacts/700-wide/gold-verify.md`
- **DQ certificate**: `Artefacts/700-wide/dq-certificate.md`
