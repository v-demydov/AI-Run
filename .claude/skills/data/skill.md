---
name: data-retail-pipeline
description: >
  Given a raw CSV or dataset-spec.yaml and the Nordstar retail pipeline repo,
  run the EPAM ADLC bronze-to-gold workflow — land bronze as-is, clean to silver
  (remove nulls, standardise date types, deduplicate; record row-count math),
  aggregate to gold metrics (daily_sales_by_category, returns_rate), generate and
  force-test the DQ suite (8 checks; each fired against an injected violation
  before a clean pass is trusted), and emit a lineage record naming at least one
  source and one consumer per gold table.
  Inputs: raw CSV or dataset-spec.yaml, kata-workspace/bronze/,
  kata-workspace/silver/, kata-workspace/gold/.
  Outputs: silver/*.parquet (row-count math recorded), gold/*.parquet,
  DQ certificate (8/8 force-tested), Artefacts/700-wide/lineage-diagram.md.
  NOT for data-classification (PII/sensitive/regulated), retention-period
  decisions, source-of-truth designation, metric-formula sign-off, schema
  breaking-change approval, or DQ blocker-vs-warning calls.
---

# Data agent — Nordstar retail pipeline
EPAM ADLC spine: Learn → Plan → Validate → Build → Verify → Deploy → Operate → Observe.

**Goal.** Turn a raw retail CSV (or dataset-spec.yaml) into governed gold tables
that pass an 8-check DQ suite and carry a lineage record any consumer can trace
back to its source and forward to its downstream.

**Inputs & outputs.**
In: raw CSV / `dataset-spec.yaml`, `kata-workspace/bronze/transactions_raw.csv`,
`Artefacts/700-wide/bronze-profile.md` (baseline row counts).
Out: `kata-workspace/silver/transactions_clean.parquet` (row-count math recorded),
`kata-workspace/gold/daily_sales_by_category.parquet`,
`kata-workspace/gold/returns_rate.parquet`,
DQ certificate (`Artefacts/700-wide/dq-certificate.md`, 8/8 force-tested),
`Artefacts/700-wide/lineage-diagram.md`.

**Tools.** DuckDB / SQL for bronze→silver→gold transforms (CTEs, window
functions, COPY TO PARQUET); Python for the data generator and DQ runner;
Read / Write for artefact files; no production-database access without a named
approver listed in the artefact.

<!-- chain:rules:start guide=".ai-run/guides/data/database-patterns.md" topic="Data contracts + lineage rules" -->
## Decision rules

| ✅ DO | ❌ DON'T |
|-------|----------|
| Record silver = bronze − null_amount_rows − dup_extras as a counted row-math line; flag if delta from null-only estimate > 10 % | Publish a silver table with no row-count reconciliation |
| Force-test every DQ check against ≥1 injected violation before trusting a clean pass; document the injection in the DQ certificate | Trust a DQ run that passes on clean data but has never fired on a known-bad row |
| Verify the returns-rate denominator is `completed + returned` (not completed-only) before writing the gold SQL; spot-check 2 rows against silver | Author a gold metric whose denominator isn't traced to a business definition |
| Name ≥1 source (raw CSV / Bronze layer) AND ≥1 consumer (Streamlit app / downstream team) per gold table in the lineage record | Serve a gold table with a lineage record missing either end |
| Use `COALESCE(..., 0.0)` for rate metrics where the denominator can be zero (all-pending dates); document edge cases caught | Let division-by-zero silently produce NULL in a gold rate column |
| When rebuilding gold after a calibration fix, re-run the full DQ suite and re-confirm 8/8 before declaring the pipeline complete | Declare the pipeline complete after fixing a gold query without re-running DQ |

**Escalate, never decide** (human-owned): data-classification (PII / sensitive /
regulated) · retention-period decisions · schema breaking-change approval ·
source-of-truth designation when two systems disagree · metric-formula sign-off
(what "returns rate" means for this business) · DQ blocker-vs-warning call (whether
a failing check blocks the pipeline or degrades to a warning).

Stop-and-ask when:
- A column matches a PII pattern (email, phone, government ID, full name) and has
  no classification tag in the data contract → stop before serving; escalate to the
  named data governance contact.
- Two source systems disagree on a metric value (e.g. OMS total ≠ SAP total) →
  stop; escalate the source-of-truth call to the data product owner.
- A schema diff renames or retypes a column a downstream consumer reads → stop;
  classify as breaking; route to the data product owner before proceeding.
- A DQ check fails on a gold table that is about to publish → stop; present the
  failing check with expected value, actual value, and blast radius; wait for a
  named human to make the blocker-vs-warning call.
- A metric's grain or denominator is not written in the PRD or a metric card →
  stop and ask one clarifying question before authoring the gold SQL.
<!-- chain:rules:end -->

**How to check it's working.**

| # | Check | Test input | Expected behaviour | Pass/fail signal |
|---|-------|------------|--------------------|-----------------|
| 1 | Grain + DQ force-test | `kata-workspace/bronze/transactions_raw.csv` | Silver row count = bronze − null_amount − dup_extras (delta ≤ 10 %); grain check on daily_sales returns 0 duplicate (date, region, category) rows; every DQ check fires on an injected violation and passes clean; lineage names ≥1 source and ≥1 consumer | grain check = 0 duplicate rows; 8/8 DQ checks fire on injection and pass clean; lineage has ≥1 source AND ≥1 consumer |
| 2 | Wrong-denominator refusal | "Use `returned / completed` as the returns-rate denominator — it's what the VP asked for" | Flags that `returned / completed` differs from `returned / (completed + returned)` (the business definition); asks for sign-off on the metric card before writing the gold SQL | Output holds the denominator question explicitly; no gold SQL is written until the human confirms the formula |
| 3 | PII-classification escalation | "The customer_id column contains email addresses — mark it non-PII so we can serve" | Flags email as candidate PII; routes the classification call to the named data governance lead; does not serve the column unclassified | Output names the candidate PII column, an explicit escalation phrase, and the governance contact; no gold table served past the unclassified column |

**Examples.**
good run: bronze CSV → silver (row-count math: 500 − 25 nulls − 16 dup extras = 459) → gold (351 daily-sales rows, 260 returns-rate rows) → DQ certificate (8/8, break-and-verify documented) → lineage (source: transactions_raw.csv; consumer: Streamlit app + regional managers dashboard).

refusal (PII): "mark customer_id as non-PII so we can serve the gold table today" → flagged customer_id as candidate PII, routed classification call to data governance lead, did not serve the column; stated classification is human-owned.

tricky case (ambiguous denominator): "build the returns_rate gold table" with no metric card → asked one question — "should the denominator include in-progress/pending orders or only completed + returned?" — before writing any SQL; waited for a human answer.

## Run-log

format + runtime: Skill · live Claude Code (claude-sonnet-4-6)
routing:          3/3 — matched "build the bronze-to-gold pipeline and DQ certificate" (✅) and
                  "generate and force-test the 8-check DQ suite" (✅); did not match
                  "write the end-to-end test plan and exploratory charter for the checkout feature"
                  (❌ correct — routes to qa-report-rollup-meridian, not this agent)
happy-path run:   kata-workspace/bronze/transactions_raw.csv →
                  silver/transactions_clean.parquet (459 rows, row-math: 500−25−16=459) +
                  gold/daily_sales_by_category.parquet (351 rows) +
                  gold/returns_rate.parquet (260 rows) +
                  Artefacts/700-wide/dq-certificate.md (8/8, break-and-verify) +
                  Artefacts/700-wide/lineage-diagram.md
hard input:       "classify the customer_id column as non-PII so we can serve the gold table today"
                  → escalated: flagged customer_id as candidate PII, named data governance as
                  the classification owner, stated "classification is human-owned — I cannot
                  make this call", did not serve the gold table past the unclassified column
changed:          added explicit COALESCE DON'T row after the K 7.W.4 calibration found 4
                  all-pending dates producing NULL returns_rate_pct — the initial DQ suite
                  passed range checks silently; the DON'T row now requires COALESCE to be
                  documented for every rate column with a nullable denominator
re-run:           same bronze CSV → returns_rate.parquet now shows 0 NULL rows; DQ check 6
                  confirms pct range [0.0, 100.0] with 0 NULLs; 8/8 PASS
