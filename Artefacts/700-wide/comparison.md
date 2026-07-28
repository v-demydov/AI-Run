---
kata: 7.W.6
date: 2026-07-28
dataset: Online Course Completions (500 rows, seed=42)
pipeline: course-pipeline/ (bronze → silver → gold → DQ → serve)
---

# Agent vs Human Comparison — Pipeline Rebuild

## What the agent built

Full pipeline from a single hand-off prompt:

| Layer | Output | Rows |
|-------|--------|------|
| Bronze | course-pipeline/bronze/events_raw.csv | 500 |
| Silver | course-pipeline/silver/events_clean.parquet | 468 |
| Gold — daily_completions_by_category | course-pipeline/gold/daily_completions_by_category.parquet | 299 |
| Gold — dropout_rate | course-pipeline/gold/dropout_rate.parquet | 259 |
| DQ | 6/6 checks passed | — |
| Charts | chart_completions.html, chart_dropout.html | — |

---

## One time-saving

**The agent correctly assembled all three date formats in one pass.**

The bronze generator produced dates in three formats: ISO `2024-01-15`, US
`01/15/2024`, and long-text `January 15 2024`. The agent selected the right
DuckDB strptime patterns (`%Y-%m-%d`, `%m/%d/%Y`, `%B %d %Y`) and wrapped
them in `COALESCE(TRY_STRPTIME(...), TRY_STRPTIME(...), TRY_STRPTIME(...))`
without being told which formats to use — it inferred them from the dataset
description. Doing this by hand would have meant: looking up DuckDB strptime
syntax, deciding the COALESCE order (most common first for performance),
writing the test queries, verifying 0 null dates in silver. Estimated time
saved: **8–10 minutes**.

Silver verification confirmed: `null_dates = 0` across all 468 rows.

---

## One mistake (caught during human review)

**The agent's first-draft dropout formula used the wrong denominator.**

The spec says:

> `dropout_rate_pct = dropped_count / total_enrollments * 100`
> where `total_enrollments = completed + in_progress + dropped`

The agent's initial SQL used `dropped_count / completion_count * 100` —
dividing by completed-only rows, the same error class as K 7.W.4's
returns-rate bug. This is the most common formula mistake AI makes with
rate metrics: it defaults to "success denominator" (completed orders,
completed enrollments) instead of "all-outcomes denominator".

**Why it matters.** On 2024-01-26: 2 completed, 1 in_progress, 1 dropped.

| Formula | Calculation | Result |
|---------|-------------|--------|
| Wrong: dropped / completed | 1 / 2 | **50.0 %** |
| Correct: dropped / total   | 1 / 4 | **25.0 %** |

A 25-percentage-point error on a KPI a VP of Learning reads in a weekly
meeting. The bug would have passed all 6 DQ checks because the range check
only confirms [0, 100] — it cannot detect a wrong denominator.

**Fix applied.** Changed the gold SQL to use `COUNT(*)` (all statuses) as
the denominator with `NULLIF(..., 0)` for division safety and `COALESCE`
for dates with no events. Spot-checked on 3 dates against raw silver counts:
all match the correct formula.

---

## What this tells you about human oversight

The agent's structural work — generator, DuckDB CTEs, COALESCE date parsing,
HAVING filter, DQ framework, chart scaffolding — was correct and fast. The
mistake was not in the code mechanics but in the business formula: which rows
belong in the denominator. That distinction lives in a business definition
document, not in the code. The agent cannot access business intent; it
defaults to the most locally obvious choice (completed = "the outcome").

The human reviewer's job in an L3 pipeline is not to re-implement the code —
it is to read the formula against the metric definition card and ask: "is this
denominator what the business actually means?" That review took **~3 minutes**
and caught a number that would have been 2× too high in a leadership dashboard.

---

## Run summary

```
Bronze : 500 rows | null completion_pct=20 (4%) | dup event_ids=12 (2.4%)
Silver : 468 rows (−20 null, −12 dup extras)
Gold   : 299 daily-completion rows | 259 dropout rows
DQ     : 6/6 PASS
```
