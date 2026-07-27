---
case: Meridian Retail Group — Click & Collect
feature: AI Availability Assistant (confidence-signal PDP label + Low-confidence modal)
date: 2026-07-27
author: QA — Sprint 1 scope review
---

# Test Plan — Click & Collect AI Availability Assistant

## In scope

1. **Velocity-adjusted confidence scoring** — High / Medium / Low label on the PDP before the shopper taps "Reserve for Click & Collect"; correct tier assignment against SAP count × OMS sync age × same-day POS sell-through rate.
2. **Binary fallback safety** — when the model cannot score (POS data absent, SAP sync stale > 4 h, or inventory ≤ 0), the UI shows the cached OMS binary state; no phantom "High" leaks through.
3. **Low-confidence warning modal** — modal fires on every "Reserve" tap when score is Low; focus-trapped dialog with initial focus on "Choose another store"; modal absent for High and Medium scores.
4. **Velocity signal gate** — model includes POS sell-through only if offline experiment shows ≥ 5% MAPE improvement; scoring degrades to SAP-only path when gate condition is not met.
5. **Screen-reader accessibility** — confidence label announced via `aria-describedby`; modal carries `role="dialog"`, `aria-modal="true"`, WCAG 2.1 AA focus trap; verified on VoiceOver (macOS/iOS) and NVDA (Windows).

## Out of scope

| Exclusion | Rationale |
|-----------|-----------|
| SAP ECC inventory ground-truth correctness | Owned by Finance IT; covered by SAP's own reconciliation controls. We test how the feature responds to counts, not whether SAP's counts are accurate. |
| Alternative store suggestions (S2) | Explicitly deferred to post-Sprint 1; no UI surface exists. |
| Confidence logging and ops dashboard (S10, S11) | Post-Sprint 1 features; excluded until surfaces are built. |

## Top 3 risks

**Risk 1 — Phantom-stock "High" on stale OMS sync**
The model emits High confidence while the OMS snapshot is within the 4-hour window but in-store inventory has already depleted; the shopper reserves an item that is gone and the order is cancelled at pickup. Business impact: the 7% cancellation rate does not fall — David Park's Black Friday runbook relies on the signal being trustworthy at peak load, and the feature's entire commercial case evaporates.

**Risk 2 — Low-confidence modal suppressed by TTL re-fetch failure**
A shopper's score is 10+ minutes old; the silent re-fetch on "Reserve" tap times out; the modal does not fire and the shopper completes the reservation unwarned. Business impact: the risk-reduction mechanism silently stops working under degraded network or peak load — exactly the moments when cancellations spike — and Asha Sundaram's 90-day ≤ 4% target is missed with no alerting.

**Risk 3 — Accessibility focus trap broken on Low-confidence modal**
VoiceOver/NVDA users hear the modal announced but Tab/Arrow navigation escapes the dialog, making "Choose another store" unreachable. Business impact: WCAG 2.1 AA violation triggers European Accessibility Act exposure across EU stores; Marco Rossi's regional pilot faces a legal blocker before launch.

## Entry criteria

1. Sprint 1 build deployed and smoke-tested on the QA region (EU-West staging); confidence label visible on at least one test PDP.
2. SAP sandbox seeded with three inventory scenarios: count > 0 with fresh sync, count > 0 with sync age > 4 h, and count ≤ 0.
3. POS sell-through stub configured for two states: data present (MAPE gate met) and data absent (SAP-only fallback active).

## Exit criteria

1. Critical-path pass rate ≥ 95% across all in-scope test cases (confidence scoring, fallback, modal, accessibility).
2. Zero phantom-stock "High" emissions on stale-OMS test cases (Risk 1 — all P1 cases must pass).
3. Named sign-off from David Park (ops runbook review) and Sarah Chen (CX acceptance) before the plan closes.
