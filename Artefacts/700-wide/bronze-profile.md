---
kata: 7.W.1
date: 2026-07-28
source: kata-workspace/bronze/transactions_raw.csv
seed: 42
---

# Bronze Profile — transactions_raw.csv

Baseline numbers recorded before any cleaning.  
Reference these in K 7.W.3 to verify silver cleaning removed the correct rows.

## Row and null counts

| Metric | Value | Note |
|--------|-------|------|
| Total rows | 500 | |
| null order_id | 0 | |
| null customer_id | 0 | |
| null region | 0 | |
| null order_date | 0 | |
| null product_category | 0 | |
| **null amount** | **25** | **5% of rows — intentional quality issue** |
| null quantity | 0 | |
| null status | 0 | |

## Duplicate order_ids

| Metric | Value | Note |
|--------|-------|------|
| Duplicate order_ids (extra copies) | 18 | `COUNT(*) - COUNT(DISTINCT order_id)`; target was ≈15 (3%) |

## Amount range

| Metric | Value |
|--------|-------|
| min_amount | -480.79 |
| max_amount | 496.52 |

Negative values (min < 0) confirm the 2% returns are present.

## Status distribution

| status | count | share |
|--------|-------|-------|
| completed | 401 | 80.2% |
| returned | 79 | 15.8% |
| pending | 20 | 4.0% |

Target split was 80 / 15 / 5 — actual is within 1 pp on all three.

## Region distribution

| region | count |
|--------|-------|
| East | 131 |
| South | 124 |
| West | 123 |
| North | 122 |

Roughly even four-way split as intended.

## Date formats present

Three formats confirmed in the raw file:

| Format | Example | Share (approx) |
|--------|---------|----------------|
| YYYY-MM-DD | 2024-01-15 | ~50% |
| DD/MM/YYYY | 15/01/2024 | ~30% |
| Mon DD YYYY | Jan 15 2024 | ~20% |

Mixed formats are intentional — silver cleaning step (K 7.W.3) standardises all dates to ISO YYYY-MM-DD.

## Profiling SQL (DuckDB)

```sql
-- Summary stats
SELECT
    COUNT(*)                                       AS row_count,
    COUNT(*) - COUNT(order_id)                    AS null_order_id,
    COUNT(*) - COUNT(customer_id)                 AS null_customer_id,
    COUNT(*) - COUNT(region)                      AS null_region,
    COUNT(*) - COUNT(order_date)                  AS null_order_date,
    COUNT(*) - COUNT(product_category)            AS null_product_category,
    COUNT(*) - COUNT(amount)                      AS null_amount,
    COUNT(*) - COUNT(quantity)                    AS null_quantity,
    COUNT(*) - COUNT(status)                      AS null_status,
    COUNT(*) - COUNT(DISTINCT order_id)           AS duplicate_order_ids,
    ROUND(MIN(amount), 2)                         AS min_amount,
    ROUND(MAX(amount), 2)                         AS max_amount
FROM read_csv_auto('bronze/transactions_raw.csv', ignore_errors=true);

-- Status distribution
SELECT status, COUNT(*) AS cnt
FROM read_csv_auto('bronze/transactions_raw.csv', ignore_errors=true)
GROUP BY status ORDER BY cnt DESC;

-- Region distribution
SELECT region, COUNT(*) AS cnt
FROM read_csv_auto('bronze/transactions_raw.csv', ignore_errors=true)
GROUP BY region ORDER BY cnt DESC;
```
