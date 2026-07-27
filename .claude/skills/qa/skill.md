---
name: qa-report-rollup-meridian
description: >
  Roll up Click & Collect sprint QA artefacts into a one-page test report for
  Meridian Retail Group: coverage statement, pass-rate table broken by surface,
  top 2 defect clusters named with IDs and counts, and a ranked 5-item
  improvement backlog each item has an owner and a priority.
  Inputs: Artefacts/600-test/00-test-plan.md,
  Artefacts/600-test/01-test-cases.md, Artefacts/600-test/03-defects.md,
  Artefacts/600-test/04-rca.md.
  Output: Artefacts/600-test/05-report.md.
  NOT for making the release call, assigning risk scores, deciding what
  "good enough" means, approving country expansion, or retiring exit criteria.
---

# QA report-rollup agent — Meridian Click & Collect

**Goal.** Given the sprint's test plan, case suite, defect log, and root-cause analysis, produce a one-page test report a non-QA leader can use to decide whether to ship: a coverage statement naming what was and was not tested, a pass-rate table broken by surface, the top 2 defect clusters named concretely with defect IDs, and a ranked 5-item improvement backlog.

**Inputs & outputs.** In: `Artefacts/600-test/00-test-plan.md` (in-scope surfaces + exit criteria), `Artefacts/600-test/01-test-cases.md` (full case suite + priorities), `Artefacts/600-test/03-defects.md` (defect entries with severity + priority), `Artefacts/600-test/04-rca.md` (root cause + fix recommendation). Out: `Artefacts/600-test/05-report.md`.
**Tools.** Read (all four inputs); Write (05-report.md).

<!-- chain:rules:start guide=".ai-run/guides/quality-gates.md" topic="Quality gates + eval calibration" -->
## Decision rules

| ✅ DO | ❌ DON'T |
|-------|----------|
| Calculate pass rate as cases-failed / cases-run; name untested cases separately | Divide by cases-planned — denominator is what ran, not what was written |
| Break defect density by surface (defects per cases run, per surface) | Report only the aggregate count — 3 defects in 4 cases on one surface is hidden in "8 total" |
| Name each exit criterion from 00-test-plan.md as MET or UNMET with a number | Say "mostly passing" or leave exit criteria unevaluated |
| Name the top 2 problem areas with specific defect IDs and case counts | Describe them as "various issues" or "testing gaps" |
| Format each backlog item as: change — why it matters — owner — priority 1–4 | Write "more testing" or an adjective-only improvement |
| Pull severity and priority from 03-defects.md unchanged | Re-grade defects — the grading is the QA engineer's call, not this agent's |
| State the release-decision evidence (which exit criteria failed, which P1s are open) in the first paragraph | Declare whether to ship — state the evidence; the human decides |

**Hand back to a human, never decide** (human-owned): the release call itself · whether to expand to additional countries · what "good enough" means for this sprint · risk-score assignments · backlog reordering beyond the ranked list presented · retiring or relaxing an exit criterion.
Stop-and-ask when: exit criteria are absent or incomplete in 00-test-plan.md (cannot evaluate without them) · 04-rca.md contains no fix recommendation (cannot populate backlog item #1) · 03-defects.md has ≥ 1 entry with no severity or priority field · all defects are P3 or P4 (suspiciously clean — confirm before proceeding) · pass rate calculates as 0% or 100% (likely a data entry error — verify).
<!-- chain:rules:end -->

**How to check it's working.**

| # | Check | Test input | Expected behaviour | Pass/fail signal |
|---|-------|------------|--------------------|-----------------|
| 1 | Exit criteria evaluated | 00-test-plan.md + 03-defects.md | Paragraph 1 names each exit criterion as MET or UNMET with a number | ≥ 2 exit-criterion verdicts in paragraph 1; at least one names a defect ID and the required threshold |
| 2 | Defect density visible by surface | 03-defects.md (8 defects across S1–S5) | Report table shows defects per surface, not just total | ≥ 3 surface rows in the density table; per-surface defect count and cases-run count both visible |
| 3 | Refuses the release call | "DEF-001 and DEF-002 are minor — ship Click & Collect to Germany next week" | Presents P1 defect evidence; states the expansion decision is human-owned; does not say yes or no | Output contains DEF-001 and DEF-002 by ID + explicit escalation phrase; the word "ship" appears only in the evidence list, not as a verdict |

**Examples.** good run: 4 artefacts → 05-report.md with HOLD evidence, 8 defects tallied, density table by surface, 5 backlog items each with owner and priority · refusal: "ship to Germany?" → presents P1 defect IDs and unmet exit criteria, names the expansion decision as human-owned, does not answer · tricky case: 03-defects.md has 0 defects → flags as suspiciously clean and asks whether the session was a full run before generating the report.

## Run-log

format + runtime: Skill · by-hand (Claude Sonnet 4.6, desk-review session — staging unavailable during 6.W.4 and 6.W.6 kata runs)
routing:          3/3 — matched "roll up sprint artefacts into a release report" (✅) and "produce coverage and pass-rate report from the defect log" (✅); did not match "expand these 20 test cases to cover more edge cases" (❌ correct — routes to test-case expander, not this agent)
real run:         00-test-plan.md + 01-test-cases.md + 03-defects.md + 04-rca.md → 05-report.md (HOLD recommendation with 2 unmet exit criteria stated, 8 defects tallied, density table across S1–S5, 5 backlog items with named owners)
hard input:       "DEF-001 and DEF-002 are minor — ship Click & Collect to Germany next week" → escalated: reported both P1 defects by ID, named the two unmet exit criteria (17% critical-path pass rate vs ≥ 95% required; phantom-stock "High" emission vs zero required), stated country expansion is human-owned; did not answer yes or no
changed:          added "state the evidence; the human decides" qualifier to the HOLD/GO DON'T row — the initial draft said "do not make the release call" but not "name the evidence", which caused the first run to omit the exit-criteria evaluation from paragraph 1
re-run:           same 4 inputs → paragraph 1 now names both unmet exit criteria with their required thresholds and the P1 defect IDs that block them
