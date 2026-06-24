---
station: 300-design
role: Design
source: own+overlay          # adapted from AI-Run/.claude/skills/design (K3 kata series, Meridian)
reads: runs/<feature-slug>/200-spec.md
writes: runs/<feature-slug>/300-design.md
mode: one-pass               # single execution; no background sub-agents; no recursive calls; no live writes during run
fallback: fallback-specs/300-design.md
---

# Station 300 — Design

## Goal

Turn a feature spec into an evidence-based flow, annotated screen states, AI-aware
acceptance criteria, and an agent-ready handoff (CONTEXT.md + SPEC.md) a coding
agent can build from without a follow-up question. One pass; escalate every judgment
call to a human.

---

## Input contract

`runs/<feature-slug>/200-spec.md` must contain:

| Field | Required |
|-------|----------|
| At least one user story (As a / I want / So that) | ✅ |
| One primary outcome metric (window + threshold + source) | ✅ |
| At least one named out-of-scope item | ✅ |
| Feasibility verdict (Branch 1 + Branch 2 from JTBD gate) | ✅ |
| Technical environment (surface, data source, auth) | ✅ |

If any field is absent, record a gap in `300-design.md` under `## Gaps` and stop.
Do not invent missing inputs.

---

## Output contract

`runs/<feature-slug>/300-design.md` must contain all five sections:

### 1 — User flow

The feature flow as a Mermaid journey or flowchart covering:
- Happy path (nominal confidence / availability state)
- At least one error / low-confidence path
- Fallback state (data unavailable)

Each step tagged with actor emotion (score 1–9) or an emotion label.

### 2 — Screen states

For each distinct UI state: component name, variant trigger, copy, and linked AC.
Minimum: happy path state + low-confidence state + fallback state.

### 3 — AI-aware AC (6 clauses)

One testable clause per AI dimension:
- Confidence (threshold: number or posterior)
- Refusal / fallback (trigger conditions: explicit, boolean)
- Latency (p95 ceiling in ms)
- Disclosure (observable copy requirement)
- Feedback (logging spec: fire-and-forget, fields, timeout)
- Negative AC (explicit "must NOT" list — ≥3 named prohibitions)

Each clause must have a threshold or observable condition. No vague adjectives.

### 4 — Agent-ready handoff

A CONTEXT block (feature, audience, environment, hard constraints, out-of-scope)
and a SPEC block (≥2 components with states + token references + negative AC carried
in as named test cases). Passes the 6-point Definition of Handoff Done (see §6).

### 5 — Gaps (optional)

Any input ambiguity, unresolvable constraint, or fired human gate that blocked a
section. Each gap: what is missing, which section it blocks, what the human must
resolve before re-run.

---

## Decision rules

| ✅ DO | ❌ DON'T |
|-------|----------|
| Name a user moment (journey step + emotion) in every How-Might-We | Write an HMW naming a feature or solution |
| Give each AI-AC clause a threshold or observable condition | Ship "user-friendly", "fast", or "accurate" as an AC |
| Close ≥1 named decision per workshop block, with a named owner | Produce a workshop section with no decision and no owner |
| Reference design tokens by exact name (`--color-confidence-high-text`) | Invent component names with no design-system parity |
| Carry negative AC ("must NOT") into SPEC as explicit named test cases | Drop the negative AC between AI-AC and SPEC |
| Run the 6-point Definition of Handoff Done before closing | Ship without the checklist |

---

## Human gates

Stop and escalate — never decide — for:

| Gate | Trigger |
|------|---------|
| **Brand judgment** | Any copy or visual pattern requiring brand voice sign-off |
| **Accessibility from lived experience** | Any trust surface or disclosure requiring AT testing beyond WCAG 2.1 AA |
| **Ethical tradeoffs** | Any pattern that could deceive, manipulate, or unfairly disadvantage a user |
| **Controversial UX patterns** | Dark patterns, forced flows, opaque defaults |
| **Strategic IA decisions** | Navigation structure, feature placement in a broader IA |
| **Sensitive copy** | Legal disclosures, error messages with duty-of-care implications |
| **Saying no to an AI feature** | Any finding that the AI capability is misplaced or harmful |

When a gate fires: record it in `## Gaps`, state the question precisely, stop.

---

## Fallback-gap instruction

If this station cannot produce a complete `300-design.md` from `200-spec.md`
(missing inputs, unresolvable ambiguity, or a fired human gate):

1. Write whatever sections can be completed.
2. Record each gap in `## Gaps` with: missing field, blocked section, resolution needed.
3. Copy `fallback-specs/300-design.md` as the design skeleton for human completion.
4. Do not emit a partial output without a `## Gaps` section.

---

## Quality check (6-point Definition of Handoff Done)

| # | Check | Pass condition |
|---|-------|---------------|
| 1 | User story + base AC present | ✅ Story in As a / I want / So that form; ≥4 base AC |
| 2 | ≥3 AI-AC refined to component/variant/token/placement/visual gate | ✅ Each has all 6 slots filled |
| 3 | CONTEXT block covers feature + audience + environment + constraints + out-of-scope | ✅ All 5 fields present |
| 4 | SPEC block lists ≥2 components with states + token references | ✅ Each component has variant table + token names |
| 5 | Asset/data reference explicit and resolvable | ✅ API path or cache source named |
| 6 | Negative AC ("must NOT") carried into SPEC as named test cases | ✅ ≥3 prohibitions, each a named test case |
