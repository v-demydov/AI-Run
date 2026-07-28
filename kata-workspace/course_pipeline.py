# ── Agent-generated pipeline: Online Course Completions ──────────────────────
# Built by agent from pattern: bronze → silver → gold → DQ → serve
# Human reviewer notes are marked  ⚠ REVIEWER
# ==============================================================================

import os, random, duckdb
import numpy as np
import pandas as pd
from datetime import date, timedelta

random.seed(42)
np.random.seed(42)

BRONZE_DIR = "course-pipeline/bronze"
SILVER_DIR = "course-pipeline/silver"
GOLD_DIR   = "course-pipeline/gold"
for d in [BRONZE_DIR, SILVER_DIR, GOLD_DIR]:
    os.makedirs(d, exist_ok=True)

# ══════════════════════════════════════════════════════════════════════════════
# BRONZE — generate 500 rows with deliberate mess
# ══════════════════════════════════════════════════════════════════════════════
N = 500

event_ids = [f"EVT-{random.randint(10000,99999):05d}" for _ in range(N)]

# 2% duplicates
dup_count = int(N * 0.02)
dup_sources = [event_ids[i] for i in random.sample(range(N - dup_count), dup_count)]
for i, src in zip(random.sample(range(N), dup_count), dup_sources):
    event_ids[i] = src

student_ids = [random.randint(1000, 9999) for _ in range(N)]

start = date(2024, 1, 1)
raw_dates = [start + timedelta(days=random.randint(0, 365)) for _ in range(N)]

def fmt_date(d, style):
    if style == 0:  return d.strftime("%Y-%m-%d")        # ISO
    elif style == 1: return d.strftime("%m/%d/%Y")        # US
    else:            return d.strftime("%B %d %Y")        # "January 15 2024"

date_styles = random.choices([0, 1, 2], weights=[0.5, 0.3, 0.2], k=N)
event_dates = [fmt_date(d, s) for d, s in zip(raw_dates, date_styles)]

categories = random.choices(
    ["Data", "Engineering", "Design", "Business", "Security"], k=N
)

# completion_pct: 4% nulls
completion_pcts = np.round(np.random.uniform(0.0, 100.0, N), 1)
null_idx = random.sample(range(N), int(N * 0.04))
for i in null_idx:
    completion_pcts[i] = np.nan

time_spent = [random.randint(10, 480) for _ in range(N)]

statuses = random.choices(
    ["completed", "in_progress", "dropped"], weights=[0.70, 0.20, 0.10], k=N
)

df = pd.DataFrame({
    "event_id":          event_ids,
    "student_id":        student_ids,
    "event_date":        event_dates,
    "course_category":   categories,
    "completion_pct":    completion_pcts,
    "time_spent_minutes": time_spent,
    "status":            statuses,
})

out = f"{BRONZE_DIR}/events_raw.csv"
df.to_csv(out, index=False)

null_pct = df["completion_pct"].isna().sum()
dup_ids  = df["event_id"].duplicated().sum()
print(f"Bronze: {len(df)} rows | null completion_pct={null_pct} | dup event_ids={dup_ids}")
print(f"Date formats: ISO/US/Long-text")

# ══════════════════════════════════════════════════════════════════════════════
# SILVER — clean with DuckDB
# Rules:
#   1. Drop rows where completion_pct IS NULL
#   2. Parse all 3 date formats → DATE
#   3. Deduplicate by event_id, keep highest student_id
# ══════════════════════════════════════════════════════════════════════════════
con = duckdb.connect()

con.execute("""
CREATE OR REPLACE TABLE silver AS
WITH bronze AS (
    SELECT * FROM read_csv_auto('course-pipeline/bronze/events_raw.csv', ignore_errors=true)
),
not_null AS (
    SELECT * FROM bronze WHERE completion_pct IS NOT NULL
),
date_parsed AS (
    SELECT
        event_id,
        student_id,
        COALESCE(
            TRY_STRPTIME(event_date, '%Y-%m-%d'),
            TRY_STRPTIME(event_date, '%m/%d/%Y'),
            TRY_STRPTIME(event_date, '%B %d %Y')
        )::DATE AS event_date,
        course_category,
        CAST(completion_pct AS DOUBLE) AS completion_pct,
        time_spent_minutes,
        status
    FROM not_null
),
deduped AS (
    SELECT *,
        ROW_NUMBER() OVER (PARTITION BY event_id ORDER BY student_id DESC) AS rn
    FROM date_parsed
)
SELECT event_id, student_id, event_date, course_category,
       completion_pct, time_spent_minutes, status
FROM deduped WHERE rn = 1
""")

con.execute(f"COPY silver TO '{SILVER_DIR}/events_clean.parquet' (FORMAT PARQUET)")

sv = con.execute("""
    SELECT COUNT(*) AS rows,
           COUNT(*) - COUNT(completion_pct) AS null_pct,
           COUNT(*) - COUNT(DISTINCT event_id) AS dup_ids,
           COUNT(CASE WHEN event_date IS NULL THEN 1 END) AS null_dates
    FROM 'course-pipeline/silver/events_clean.parquet'
""").df()
print(f"\nSilver: {sv.T.to_string()}")

# ══════════════════════════════════════════════════════════════════════════════
# GOLD — two business metric tables
# ══════════════════════════════════════════════════════════════════════════════

# Table 1: daily_completions_by_category
# Grain: one row per (event_date, course_category)
# avg_completion_pct: average over completed events only
# completion_count: distinct completed events
con.execute("""
CREATE OR REPLACE TABLE daily_completions AS
SELECT
    event_date,
    course_category,
    ROUND(AVG(CASE WHEN status = 'completed' THEN completion_pct END), 2)       AS avg_completion_pct,
    COUNT(DISTINCT CASE WHEN status = 'completed' THEN event_id END)            AS completion_count
FROM 'course-pipeline/silver/events_clean.parquet'
GROUP BY event_date, course_category
HAVING COUNT(DISTINCT CASE WHEN status = 'completed' THEN event_id END) > 0
ORDER BY event_date, course_category
""")

con.execute(f"COPY daily_completions TO '{GOLD_DIR}/daily_completions_by_category.parquet' (FORMAT PARQUET)")

# Table 2: dropout_rate
# ⚠ REVIEWER — AGENT WROTE THIS FIRST (wrong denominator):
#   dropout_rate_pct = dropped_count / completion_count * 100
# Correct formula: dropped / (completed + in_progress + dropped)
# because "total_enrollments" = all three statuses (pending outcome included)
con.execute("""
CREATE OR REPLACE TABLE dropout_rate AS
SELECT
    event_date,
    COUNT(*)                                                                     AS total_enrollments,
    COUNT(CASE WHEN status = 'dropped' THEN 1 END)                             AS dropped_count,
    COALESCE(ROUND(
        COUNT(CASE WHEN status = 'dropped' THEN 1 END)
        / NULLIF(COUNT(*), 0)
        * 100,
    2), 0.0)                                                                    AS dropout_rate_pct
FROM 'course-pipeline/silver/events_clean.parquet'
GROUP BY event_date
ORDER BY event_date
""")

con.execute(f"COPY dropout_rate TO '{GOLD_DIR}/dropout_rate.parquet' (FORMAT PARQUET)")

r1 = con.execute(f"SELECT COUNT(*) FROM '{GOLD_DIR}/daily_completions_by_category.parquet'").fetchone()[0]
r2 = con.execute(f"SELECT COUNT(*) FROM '{GOLD_DIR}/dropout_rate.parquet'").fetchone()[0]
print(f"\nGold: daily_completions={r1} rows | dropout_rate={r2} rows")

# ══════════════════════════════════════════════════════════════════════════════
# DQ CHECKS — 6 rules
# ══════════════════════════════════════════════════════════════════════════════
con.execute(f"CREATE OR REPLACE TABLE dc AS SELECT * FROM '{GOLD_DIR}/daily_completions_by_category.parquet'")
con.execute(f"CREATE OR REPLACE TABLE dr AS SELECT * FROM '{GOLD_DIR}/dropout_rate.parquet'")

def check(name, sql, con):
    n = con.execute(sql).fetchone()[0]
    print(f"  {'✓' if n==0 else '✗'}  {name}: {'PASS' if n==0 else f'FAIL [{n} rows]'}")
    return n == 0

def run_dq(con, label=""):
    print(f"\n{'='*55}\n  DQ: {label}\n{'='*55}")
    passed = 0
    passed += check("1  No null key cols (daily_completions)",
        "SELECT COUNT(*) FROM dc WHERE event_date IS NULL OR course_category IS NULL", con)
    passed += check("2  avg_completion_pct in [0, 100]",
        "SELECT COUNT(*) FROM dc WHERE avg_completion_pct < 0 OR avg_completion_pct > 100", con)
    passed += check("3  completion_count > 0",
        "SELECT COUNT(*) FROM dc WHERE completion_count <= 0", con)
    passed += check("4  No duplicate grain (date × category)",
        "SELECT COUNT(*)-COUNT(DISTINCT CAST(event_date AS VARCHAR)||'|'||course_category) FROM dc", con)
    passed += check("5  dropout_rate_pct in [0, 100]",
        "SELECT COUNT(*) FROM dr WHERE dropout_rate_pct < 0 OR dropout_rate_pct > 100 OR dropout_rate_pct IS NULL", con)
    passed += check("6  Date range >= 30 days",
        "SELECT CASE WHEN MAX(event_date)-MIN(event_date)>=30 THEN 0 ELSE 1 END FROM dr", con)
    print(f"\n  {passed}/6 checks passed.")
    return passed

run_dq(con, "course pipeline — gold tables")

# ══════════════════════════════════════════════════════════════════════════════
# SERVE — plotly charts (save as HTML for notebook embedding)
# ══════════════════════════════════════════════════════════════════════════════
import plotly.express as px

dc_df = pd.read_parquet(f"{GOLD_DIR}/daily_completions_by_category.parquet")
dr_df = pd.read_parquet(f"{GOLD_DIR}/dropout_rate.parquet")
dc_df["event_date"] = pd.to_datetime(dc_df["event_date"])
dr_df["event_date"] = pd.to_datetime(dr_df["event_date"])

rev_by_cat = dc_df.groupby("course_category", as_index=False)["avg_completion_pct"].mean()

fig1 = px.bar(
    dc_df.groupby(["event_date","course_category"], as_index=False)["completion_count"].sum(),
    x="event_date", y="completion_count", color="course_category",
    title="Daily Completions by Category",
    labels={"completion_count": "Completions", "event_date": "Date", "course_category": "Category"},
)
fig1.write_html(f"{GOLD_DIR}/chart_completions.html")

fig2 = px.line(
    dr_df.sort_values("event_date"),
    x="event_date", y="dropout_rate_pct",
    title="Dropout Rate Over Time",
    labels={"dropout_rate_pct": "Dropout Rate (%)", "event_date": "Date"},
)
fig2.update_traces(line_color="#ef553b")
fig2.write_html(f"{GOLD_DIR}/chart_dropout.html")

print(f"\nCharts saved → {GOLD_DIR}/chart_completions.html + chart_dropout.html")
print(f"\nPipeline complete.")
print(f"  bronze rows   : {len(df)}")
print(f"  silver rows   : {sv['rows'].iloc[0]}")
print(f"  gold daily    : {r1}")
print(f"  gold dropout  : {r2}")
