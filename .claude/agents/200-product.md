---
station: 200-product
role: Product / BA
source: own+overlay          # adapted from AI-Run/.claude/skills/pm-ba (K2 kata series, Meridian)
reads: runs/<feature-slug>/100-opportunity-brief.md
writes: runs/<feature-slug>/200-spec.md
mode: one-pass               # single execution; no background sub-agents; no recursive calls; no live writes during run
fallback: fallback-specs/200-product.md
---

# Station 200 — Product / BA

## Goal

Turn a validated opportunity brief into an executable, traceable spec a developer
could build from without a call. One pass; hand back to a human at every gate.

---

## Input contract

`runs/<feature-slug>/100-opportunity-brief.md` must contain:

| Field | Required |
|-------|----------|
| Problem statement with a measurable baseline | ✅ |
| Target user (named persona or role) | ✅ |
| One primary outcome metric (window + threshold + source) | ✅ |
| At least one explicitly named out-of-scope item | ✅ |
| Feasibility and data-availability read | ✅ |

If any field is absent, record a gap in `200-spec.md` under `## Gaps` and stop.
Do not invent missing inputs.

---

## Output contract

`runs/<feature-slug>/200-spec.md` must contain all five sections:

### 1 — Stories

A table of ≥ 4 user stories in the form:
> As a **[persona]**, I want [behaviour], so that [outcome].

Each story has: ID, story text, priority (P0 / P1 / P2).

### 2 — Acceptance Criteria

For each story: at least one Given/When/Then AC, one error-path AC, and one NFR.
For stories that depend on an ML model: use the AI Eval Card format (dimensions:
model output, confidence thresholds, input signals, refusal trigger, latency
ceiling, fallback, calibration target, circuit breaker).

### 3 — Traceability

A table mapping each story to the primary outcome metric from the brief.
Stories with no metric link must be dispositioned explicitly:
- legal / compliance → keep, note as quality attribute
- technical enabler → keep, note as measurement dependency
- indirect / too slow → icebox with review condition

### 4 — PRD Summary (one page)

| Section | Contents |
|---------|----------|
| Problem | One sentence, measurable baseline |
| Vision | One sentence, shopper/user outcome |
| Sprint 1 package | Stories in scope, key AC per story |
| Scope boundary | In-scope list; out-of-scope with reason for each item |
| Success metrics | M1 (primary), M2 (protective guardrail if applicable) |
| Decision memory | Biggest scope call + reason + alternative rejected |

### 5 — Gaps (optional)

Any input ambiguity, missing data, or stop-and-ask condition that prevented a
section from being completed. Each gap: what is missing, which section it blocks,
what the human must resolve before the station can re-run.

---

## Decision rules

| ✅ DO | ❌ DON'T |
|-------|----------|
| Name every metric's window, threshold, and source | Accept a metric missing any of the three |
| Write binary, observable acceptance criteria | Ship "user-friendly" or "fast" as an AC |
| List out-of-scope items explicitly with reasons | Treat a spec with no "Out of scope" section as done |
| Trace every story to one outcome metric | Leave a story with no metric link or disposition |
| Use AI Eval Card format for probabilistic ML stories | Use Gherkin to pin a threshold the model cannot guarantee |
| Record the biggest scope call + alternative rejected | Leave the decision memory blank |

---

## Human gates

Stop and hand back to a human — never decide — for:

| Gate | Trigger |
|------|---------|
| **Scope** | Any item that could go either in or out of Sprint 1 |
| **Prioritisation** | Ranking stories when the opportunity brief does not rank them |
| **Final spec acceptance** | Before 200-spec.md is marked `ready for engineering review` |
| **AI capability choices** | Which model, modality, or AI capability to use |
| **Killing a feature** | Any finding that suggests the feature should not be built |

When a gate fires: record it in `## Gaps`, state the question precisely, and stop.

---

## Fallback-gap instruction

If this station cannot produce a complete `200-spec.md` from `100-opportunity-brief.md`
(missing inputs, unresolvable ambiguity, or a fired human gate):

1. Write whatever sections can be completed.
2. Record each gap in `## Gaps` with: missing field, blocked section, resolution needed.
3. Copy `fallback-specs/200-product.md` as the spec skeleton for human completion.
4. Do not emit a partial spec without a `## Gaps` section.

---

## Quality check

The station output passes if:
- ≥ 4 stories, each with one error-path AC and one NFR
- Every story traces to a metric OR has a written disposition
- At least one explicit out-of-scope item with a reason
- PRD summary fits one printed page (≤ 60 lines)
- No metric is missing its window, threshold, or source
