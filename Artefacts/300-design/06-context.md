---
feature: availability-confidence
kata: 3.W.7
date: 2026-06-24
handoff-for: AI coding agent / Three-Amigos review
sources: 04-ai-ac.md · 05-mockup.html · 03-decision.md
---

# CONTEXT — Availability Confidence Feature

## Feature (one sentence)

Replace the binary "In stock" label on the click-and-collect product page with a three-state confidence indicator (High / Medium / Low) derived from same-day POS velocity and SAP inventory count, paired with a friction modal that intercepts the Reserve tap when the nearest store's confidence is Low.

---

## Who uses it

| Actor | Context | Device |
|-------|---------|--------|
| Click-and-collect shopper | Deciding whether to make a pickup trip before reserving | Mobile (primary), desktop (secondary) |
| QA engineer | Verifying AI-AC thresholds, fallback states, circuit-breaker behaviour | Desktop |

The feature does NOT surface to store associates or ops managers in this release. See `06-traceability.md` (200-PRD) for deferred stories.

---

## Technical environment

| Field | Value |
|-------|-------|
| Surface | Product detail page — availability section |
| Data source | OMS confidence API (async, p95 ≤ 800ms) |
| Fallback source | Cached OMS snapshot (TTL ≤ 30 min); NOT live SAP calls |
| Auth | Non-PII path — no customer identity in API request |
| AI tools permitted | EPAM CodeMie, Claude, GPT, Gemini (anonymised inputs only) |
| Framework | As per existing product-page stack (agent: confirm before assuming) |
| Accessibility target | WCAG 2.1 AA |

---

## Hard constraints

| # | Constraint | Source |
|---|-----------|--------|
| C1 | Confidence label must load asynchronously — must NOT block page render | AI-AC3 |
| C2 | "High" label must NOT render when SAP count ≤ 0, SAP sync > 4h, or rolling 24h High-correctness < 75% | AI-AC6 |
| C3 | No language implying a physical hold ("reserved for you", "guaranteed", "confirmed in stock") | AI-AC4, AI-AC6 |
| C4 | Initial focus in FrictionModal must be "Choose another store" button — not "Reserve anyway" | AI-AC4, WCAG 2.1 AA |
| C5 | Logging write at reservation must be fire-and-forget — must NOT block reservation API response | AI-AC5 |
| C6 | Fallback path reads cached OMS snapshot — must NOT call live SAP | AI-AC2 |

---

## Out of scope (this handoff)

| Item | Why |
|------|-----|
| Alternative store suggestions | Deferred — blocked on S1 calibration data (see 05-backlog.csv S2) |
| Home delivery fallback | Requires checkout integration (S5, post-S2) |
| Associate counter tool | Ops tooling, separate workstream (C-i1 from 02-workshop.md) |
| Confidence logging dashboard | Icebox S10; review after 90 days S1 data |
| Committed item hold | Permanently out of scope — SKU depth incompatible |

---

## Related artifacts

| Artifact | Path | What it contains |
|----------|------|-----------------|
| AI-AC clauses (all 6) | `300-design/04-ai-ac.md` | Thresholds, fallback conditions, circuit-breaker, negative AC |
| Clickable prototype | `300-design/05-mockup.html` | 3-scenario flow: High / Low / Fallback |
| Decisions | `300-design/03-decision.md` | Chosen change + runner-up rationale |
| Stories + ACs (full) | `200-PRD/04-stories-acs.md` | S1 AI Eval Card v2, S4 modal AC, S7 fallback AC |
| PRD | `200-PRD/06-prd.md` | Scope boundary, success metrics M1/M2 |
