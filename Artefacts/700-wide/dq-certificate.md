---
kata: 7.W.4
date: 2026-07-28
pipeline: Nordstar Customer 360 Bronze→Silver→Gold
tables:
  - kata-workspace/gold/daily_sales_by_category.parquet
  - kata-workspace/gold/returns_rate.parquet
result: CERTIFIED — 8/8 checks passed, break-and-verify completed
---

# DQ Certificate — Gold Layer

## Run 1: clean baseline — 8/8 PASS

```
  ✓  1  No null key cols (daily_sales): PASS
  ✓  2  total_revenue > 0: PASS
  ✓  3  order_count > 0: PASS
  ✓  4  No duplicate grain (date·region·category): PASS
  ✓  5  No null order_date (returns_rate): PASS
  ✓  6  returns_rate_pct in [0, 100]: PASS
  ✓  7  returned_orders <= total_orders: PASS
  ✓  8  Date range spans >= 30 days: PASS

  8/8 checks passed.
```

## Run 2: after bad-row injection — 5/8 (3 expected failures)

Injected rows:
- `(-999.99 revenue, North, Electronics, 2024-06-15)` — negative total_revenue
- `(150.00, North, Electronics, 2024-06-15)` — duplicate grain key
- `(NULL order_date, South, Clothing, 75.00)` — null key column

```
  ✗  1  No null key cols (daily_sales): FAIL  [1 violating row(s)]
  ✗  2  total_revenue > 0: FAIL  [1 violating row(s)]
  ✓  3  order_count > 0: PASS
  ✗  4  No duplicate grain (date·region·category): FAIL  [2 violating row(s)]
  ✓  5  No null order_date (returns_rate): PASS
  ✓  6  returns_rate_pct in [0, 100]: PASS
  ✓  7  returned_orders <= total_orders: PASS
  ✓  8  Date range spans >= 30 days: PASS

  5/8 checks passed.
```

All three injected violations fired on the expected checks. Check #4 reports 2 rows because the duplicate key occupies two rows (original + injected copy).

## Run 3: after cleanup — 8/8 PASS

```
  8/8 checks passed.
```

## Gold table rebuild notes

During baseline calibration, the original gold query produced two classes of invalid rows that required fixing before the DQ suite could pass on clean data:

| Issue | Count | Root cause | Fix |
|-------|-------|-----------|-----|
| `order_count = 0` rows | 87 | Gold SQL grouped all (date, region, category) combos including those with only returned/pending orders | Added `HAVING order_count > 0` |
| `total_revenue < 0` rows | 5 | 5 synthetic rows had `status='completed'` with negative `amount` — contradicts the business rule that completed orders have positive amounts | Changed filter to `status='completed' AND amount > 0` |

Both are legitimate DQ catches: a "daily_sales" grain slot with zero completed orders should not exist, and a completed order with negative revenue is a source-system anomaly.

Final gold row counts after rebuild: `daily_sales_by_category` = 351 rows, `returns_rate` = 260 rows.

## Check catalogue

| # | Table | Rule | Dimension |
|---|-------|------|-----------|
| 1 | daily_sales | No NULL in order_date, region, product_category | Completeness |
| 2 | daily_sales | total_revenue > 0 | Validity |
| 3 | daily_sales | order_count > 0 | Validity |
| 4 | daily_sales | No duplicate (order_date, region, product_category) | Uniqueness |
| 5 | returns_rate | No NULL order_date | Completeness |
| 6 | returns_rate | returns_rate_pct in [0, 100] | Validity |
| 7 | returns_rate | returned_orders <= total_orders | Consistency |
| 8 | returns_rate | Date range spans >= 30 days | Freshness/coverage |
