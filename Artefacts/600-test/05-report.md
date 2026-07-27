---
kata: 6.W.6
consumes_from: 6.W.5
date: 2026-07-27
sprint: Sprint 1
release_decision: HOLD
---

# Test Report — Click & Collect AI Availability Assistant
### Meridian Retail Group · Sprint 1 · QA Sign-off Gate

**Release recommendation: HOLD.** Two P1 safety-class defects (DEF-001, DEF-002) are unresolved. Both mandatory exit criteria — zero phantom-stock "High" emissions and ≥ 95% critical-path pass rate — are unmet. Named sign-off from David Park and Sarah Chen is blocked until P1s are closed and the 10 untested cases are re-run against a live staging environment.

---

## 1. Coverage

**Tested**: velocity-adjusted confidence scoring (High / Medium / Low label on PDP), binary fallback safety (OMS binary state when model cannot score), Low-confidence warning modal (focus order, focus trap, dismiss flow), and screen-reader accessibility (VoiceOver aria-describedby, NVDA modal announcement, keyboard focus trap). Tested across 15 synthetic customer records spanning 10 country codes (IT, DE, JP, GB, US, ES, AE, SE, FR, NL), 10 distinct payment methods (including Klarna split-pay and Postepay), 4 language scripts (Latin, Latin-Extended, CJK/kana, Arabic RTL), and 4 identity states (clean, merged, anonymous, expired loyalty). Test method: structured desk review against `02-test-data.json`; QA EU-West staging was offline during this session — no live browser execution was performed and all defect findings require live Playwright confirmation before promotion to the sprint board.

**Not tested**: velocity signal gate (S4 — TC-13 through TC-16 not run), SAP ECC inventory ground-truth correctness (owned by Finance IT), alternative store suggestions (S2, deferred to post-Sprint 1), confidence logging and ops dashboard (S10/S11, post-Sprint 1), cross-region multi-currency settlement, Phase 2 cross-channel inventory reservation patterns, Satispay / iDEAL SCA interaction with the Low-confidence modal, and the 10 cases not run from the 20-case suite (TC-02, TC-03, TC-06, TC-10, TC-11, TC-13–TC-16, TC-18).

---

## 2. Pass rate and defect density

**Overall (10 of 20 cases run):**

| Metric | Value |
|--------|-------|
| Cases run | 10 / 20 |
| Cases passed | 3 / 10 (30%) |
| Cases failed | 7 / 10 (70%) |
| Unique defects found | 8 |
| Defect density | 0.5 per case run |

**Critical-path pass rate (exit criterion: ≥ 95%):**

| Category | Cases run | Passed | Failed | Pass rate |
|----------|-----------|--------|--------|-----------|
| Critical-path P1 | 6 | 1 | 5 | **17%** ← unmet |
| Smoke P1 | 2 | 1 | 1 | 50% |
| Edge P2 | 2 | 1 | 1 | 50% |

**Phantom-stock "High" emissions (exit criterion: zero):**

DEF-001 confirms phantom "High" emitted on stale-OMS + SAP = 0 scenario. **Exit criterion not met.**

**Defect breakdown by surface:**

| Surface | Cases run | Defects | Density | P1 defects |
|---------|-----------|---------|---------|------------|
| S1 + S2 — Confidence scoring + fallback | 4 | 1 (DEF-001) | 0.25 / case | 1 |
| S3 — Low-confidence modal | 3 | 2 (DEF-002, DEF-003) | 0.67 / case | 1 |
| S5 — Accessibility | 3 | 2 (DEF-004, DEF-007) | 0.67 / case | 0 |
| S4 — Velocity signal gate | 0 | 0 | not run | — |
| Cross-cutting (identity, error handling, locale) | — | 3 (DEF-005, DEF-006, DEF-008) | — | 0 |

**Defects by priority:**

| Priority | Count | Defect IDs | Unblocks exit criteria? |
|----------|-------|------------|------------------------|
| P1 — fix before release | 2 | DEF-001, DEF-002 | Yes — both block sign-off |
| P2 — fix this sprint | 4 | DEF-003, DEF-004, DEF-005, DEF-006 | Partial |
| P3 — next sprint | 2 | DEF-007, DEF-008 | No |

---

## 3. Top 2 problematic areas

**Area 1 — Phantom-stock detection: scoring model bypasses the SAP ≤ 0 gate when OMS is within the freshness window.**
DEF-001 (P1/S1) shows the model emits "High confidence" on a zero-stock SKU because the OMS binary signal short-circuits the `sap_count ≤ 0` fallback check. The root cause (from `04-rca.md`): the SAP count gate sits inside the OMS freshness branch rather than before it. This is the single defect most likely to produce a customer arriving at the store with no item, a cancelled order, and no refund initiated automatically. It hits David Park's 7 % cancellation baseline directly and must be resolved before any Phase 1 country expansion.

**Area 2 — Modal safety path: two of three modal test cases fail, on different failure modes.**
DEF-002 (P1/S1): TTL re-fetch timeout is swallowed silently — the Low-confidence modal does not fire when a stale score expires under degraded network conditions (the exact moment it is most needed). DEF-003 (P2/S2): when the modal does fire, initial keyboard focus lands on "Continue anyway" rather than "Choose another store", making the unsafe default action the path of least resistance. Together these two defects mean the modal safety mechanism is unreliable both when it should trigger (DEF-002) and in how it guides behaviour when it does (DEF-003). Asha Sundaram's 90-day ≤ 4 % cancellation target depends on both being fixed.

---

## 4. Improvement backlog (ranked by impact)

1. **Restructure the scoring model entry gate so `sap_count ≤ 0` runs as an unconditional pre-check before any OMS signal is read** — closes DEF-001 (phantom-stock "High"), satisfies the zero-phantom-emission exit criterion, and unblocks David Park's sign-off — Engineering (scoring service owner) — **P1**.

2. **Change the TTL re-fetch timeout handler to fire the Low-confidence modal as a precaution rather than proceeding silently** — closes DEF-002, converts a fail-silent path into a fail-safe, and is required to meet Asha Sundaram's 90-day ≤ 4 % cancellation target — Engineering (BFF / modal service owner) — **P1**.

3. **Enforce AMBIGUOUS_IDENTITY error on merged loyalty lookups and block reservation until identity is resolved** — closes DEF-005 (cross-customer points accrual, GDPR Art. 5(1)(f) integrity exposure), required before any market with high loyalty-card churn (FR, IT) enters Phase 2 — Engineering + Privacy (Asha Sundaram's office) — **P1** (legal exposure; not gating Phase 1 launch but must ship before Phase 2).

4. **Swap modal initial focus to "Choose another store" and verify Tab trap holds for ≥ 5 cycles in NVDA and VoiceOver** — closes DEF-003 (wrong default action) and DEF-004 (focus escape), satisfies WCAG 2.1 AA SC 2.1.2, and removes the European Accessibility Act blocker for Marco Rossi's EU pilot — Frontend Engineering + Accessibility — **P2**.

5. **Add `X-Model-Version` to the confidence-scoring API response and surface it in the QA debug overlay** — closes Story S1 (model version not pinned or observable), ensures defects against a specific model version remain reproducible after the week-3 model update, and gives QA a stable reproduction anchor for every AI-surface defect — Engineering (scoring service) + QA — **P2**.

---

## Appendix — Cases not run this session

TC-02, TC-03, TC-06, TC-10, TC-11, TC-13, TC-14, TC-15, TC-16, TC-18. Cover: German-locale label rendering, OMS boundary at 3 h 59 m, zero-stock binary, modal dismiss flow, TTL near-boundary (9 m 45 s), velocity gate at all three states (gate met, gate not met, boundary exactly 5.0 %), and NVDA announcement. Must be run in the next staging session before the report can be closed.
