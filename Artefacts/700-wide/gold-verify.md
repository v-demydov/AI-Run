---
kata: 7.W.3
date: 2026-07-28
inputs:
  - kata-workspace/silver/transactions_clean.parquet
outputs:
  - kata-workspace/gold/daily_sales_by_category.parquet
  - kata-workspace/gold/returns_rate.parquet
---

# Gold Verification — Grain + Formula Spot-check

## Table 1: daily_sales_by_category

**Business definition.** One row per `(order_date, region, product_category)`.  
`total_revenue` = SUM(amount) WHERE status = 'completed'.  
`order_count` = COUNT(DISTINCT order_id) WHERE status = 'completed'.  
Pending and returned rows are excluded from revenue and order count.

### Grain check

```sql
SELECT
    COUNT(*) AS total,
    COUNT(DISTINCT order_date || '|' || region || '|' || product_category) AS unique_combos
FROM 'gold/daily_sales_by_category.parquet'
```

| Metric | Value |
|--------|-------|
| total rows | 443 |
| unique (date, region, category) combos | 443 |
| **Grain check** | **PASS** — total = unique_combos |

## Table 2: returns_rate

**Business definition.**  
`total_orders` = completed + returned (pending excluded — not yet finalised).  
`returned_orders` = status = 'returned'.  
`returns_rate_pct` = returned_orders / NULLIF(total_orders, 0) × 100, COALESCE to 0.0.  
Denominator explicitly **excludes pending** to avoid understating the rate.

### Spot-check — row 1: 2024-01-02

Silver breakdown for this date:

| status | count |
|--------|-------|
| completed | 1 |
| returned | 1 |

Manual calculation: 1 / (1 + 1) × 100 = **50.0 %**  
Gold value: **50.0 %** → **MATCH**

### Spot-check — row 2: 2024-01-12

Silver breakdown for this date:

| status | count |
|--------|-------|
| completed | 1 |
| returned | 1 |

Manual calculation: 1 / (1 + 1) × 100 = **50.0 %**  
Gold value: **50.0 %** → **MATCH**

### Edge-case: zero returns

Date 2024-01-04: total_orders = 2, returned_orders = 0.  
returns_rate_pct = **0.0** (not NULL) → **PASS**

### Edge-case: all-pending dates (division-by-zero)

4 dates had only pending orders → total_orders = 0 → NULLIF triggers → COALESCE converts to 0.0.  
NULL rows after fix: **0** → **PASS**

### Range check

| Metric | Value |
|--------|-------|
| min(returns_rate_pct) | 0.0 |
| max(returns_rate_pct) | 100.0 |
| NULL count | 0 |
| **Range check** | **PASS** — all values in [0, 100] |

## Fix applied during verification

**Original issue.** Four dates with only `pending` orders produced `total_orders = 0` in the denominator.
`NULLIF(0, 0)` correctly returned NULL, but the NULL propagated to `returns_rate_pct`.  
**Fix.** Wrapped the expression in `COALESCE(..., 0.0)` so all-pending dates report 0.0 %.  
This matches the business definition: a day with no completed/returned orders has a 0 % return rate.

## Wrong-denominator guard

Common AI error: `returned_orders / completed_orders` instead of `returned_orders / (completed + returned)`.  
Verified correct: the SQL uses `COUNT(CASE WHEN status IN ('completed', 'returned') THEN 1 END)` as denominator.  
On 2024-01-02 this matters: completed=1, returned=1 → wrong denominator gives 100 %; correct gives 50 %.
