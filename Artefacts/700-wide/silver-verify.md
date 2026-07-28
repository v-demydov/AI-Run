---
kata: 7.W.2
date: 2026-07-27
source: kata-workspace/silver/transactions_clean.parquet
bronze_source: kata-workspace/bronze/transactions_raw.csv
seed: 42
---

# Silver Verification — transactions_clean.parquet

Math check confirming the silver cleaning step removed the correct rows.

## Verification query output

```
silver_rows          459
null_amount            0
duplicate_order_ids    0
negative_amounts       9
```

## Row-count math

| Step | Rows | Note |
|------|------|------|
| Bronze total | 500 | seed=42 |
| − null amount rows | 25 | 5% of rows, dropped per rule 1 |
| − duplicate extras | 16 | from 18 recorded in bronze-profile.md; 2 dup order_ids happened to fall in the 25 null-amount rows and were removed there |
| **= Silver actual** | **459** | matches query output |

Delta from null-only estimate: **3.4%** (threshold ≤ 10% → PASS)

## Cleaning rules applied

| Rule | Result |
|------|--------|
| Drop rows where `amount IS NULL` | 25 rows removed |
| Standardise `order_date` to DATE (3 formats via `COALESCE + TRY_STRPTIME`) | All dates parsed; 0 NULLs in output |
| Deduplicate by `order_id`, keep highest `customer_id` | 16 extra copies removed |
| Retain negative amounts (valid returns) | 9 negative rows kept |

## Why dup_removed = 16, not 18

The bronze profile recorded 18 extra copies (rows beyond the first occurrence of each duplicated `order_id`).
Two of those extras belonged to rows that also had `amount IS NULL`, so they were already removed in the
null-drop step before deduplication ran. The window function therefore only had 16 extras left to eliminate.

## Silver schema confirmed

Columns: `order_id`, `customer_id`, `region`, `order_date` (DATE), `product_category`, `amount` (DOUBLE), `quantity`, `status`

File written: `kata-workspace/silver/transactions_clean.parquet`
