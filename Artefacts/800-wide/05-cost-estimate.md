---
kata: 8.W.5
date: 2026-07-30
service: cart-api
ai_model_pricing: $2.50 / M input · $10.00 / M output (Claude 3-tier reference rate; re-verify against live DIAL price list before budget sign-off)
---

# Monthly Cost Estimate — cart-api

## Inputs

| Item | Value |
|------|-------|
| AI model — input price | $2.50 / M tokens |
| AI model — output price | $10.00 / M tokens |
| AI input tokens per call | 1,200 (system prompt + cart contents) |
| AI output tokens per call | 200 (summary response) |
| AI calls per month | 3,000,000 |
| Cloud rent | $1,500 / month (flat: 3 pods + Postgres + Redis + load balancer) |

---

## Line-by-line arithmetic

### Cloud rent (flat)

| Component | Cost |
|-----------|------|
| 3 × cart-api pods (compute) | |
| 1 × Postgres (managed DB) | |
| 1 × Redis (managed cache) | |
| 1 × Load balancer | |
| **Subtotal — cloud rent** | **$1,500 / month** |

_Flat: does not scale with AI call volume or cart traffic._

---

### AI meter (scales with traffic)

| Line | Calculation | Result |
|------|-------------|--------|
| Input tokens / month | 3,000,000 calls × 1,200 tokens/call | 3,600,000,000 tokens = 3,600 M |
| Input cost | 3,600 M × $2.50 / M | **$9,000** |
| Output tokens / month | 3,000,000 calls × 200 tokens/call | 600,000,000 tokens = 600 M |
| Output cost | 600 M × $10.00 / M | **$6,000** |
| **Subtotal — AI meter** | | **$15,000 / month** |

**Hand-check:** 3,000,000 × 1,200 × $2.50 / 1,000,000 = $9,000 input alone. Any total under $5,000 would mean the call volume was dropped in the calculation.

---

### Total

| Bucket | Amount | Share |
|--------|--------|-------|
| Cloud rent (flat) | $1,500 | 9 % |
| AI meter (variable) | $15,000 | 91 % |
| **Monthly total** | **$16,500** | 100 % |

---

## Cost split and attribution

**The AI meter is 10× the cloud rent.** A 2× traffic spike doubles the AI line to $30,000 but leaves cloud rent flat. An unguarded summarise loop (e.g. retry storm, misconfigured batch job) that generates 10M calls in a day would add $50,000 in 24 hours — the scenario that hit Team A.

| Bucket | Owner | P&L |
|--------|-------|-----|
| Cloud rent — pods, Postgres, Redis, LB | Platform / Ops | Platform budget |
| AI meter — summarise feature | Cart product team | Cart feature P&L |

The AI spend is the cart team's meter to own, not a shared platform cost. It moves with their feature decisions (token budget, call rate, whether they stream or buffer).

---

## Recommendation

**Ship with mitigation.**

The $16,500/month total is within budget at current call volume (3M/month). The risk is not today's number — it is the uncapped meter. The AI line (91% of spend) has no ceiling in the current architecture. A retry storm, a misconfigured nightly batch, or a 3× traffic spike turns a $15,000 line into $45,000 or more with no automatic stop.

Mitigation required before ship:
1. Set a DIAL hard cap (see below).
2. Add `alert_threshold` below the cap so the team hears about overrun before the hard refusal hits production.
3. Stream the LLM response (see Kata 8.W.4 durable fix) — reduces per-call output latency and per-call memory, but does not reduce token cost directly.

---

## DIAL cost-cap configuration

```yaml
# EPAM DIAL gateway — cart-api cost controls
service: cart-api
ai_spend_controls:
  hard_cap_usd_per_month: 16000   # ~7 % headroom above current $15,000 AI meter
  alert_threshold_usd_per_month: 12000  # fires at 80 % of cap
  alert_channel: pagerduty://cart-api-oncall
  on_cap_exceeded: reject_with_429   # return HTTP 429 to cart-api; do NOT silently swallow
```

**Why these numbers:**

| Threshold | Value | Rationale |
|-----------|-------|-----------|
| Hard cap | $16,000 / month | Covers current AI meter ($15,000) with one month's modest growth headroom; rejects the loop scenario before it reaches the $18,000 Team A figure |
| Alert | $12,000 / month | 80 % of cap — fires early enough for the team to investigate and adjust before hitting the hard stop in production |

**Cap with no alert below it is a failed cap.** The first signal should be an alert, not a production 429. The gap between $12,000 and $16,000 is the investigation window.

---

## What to re-check before budget sign-off

1. **Live DIAL price list** — the $2.50/$10.00 rates above are reference values; the actual negotiated rate for this workspace may differ. A 20% discount on output tokens saves $1,200/month at this volume.
2. **Call volume growth** — at 3M/month today, the alert fires at 2.4M calls. If the product roadmap adds batch summarisation, re-run this estimate before the next deploy.
3. **Token budget per call** — the 1,200 input figure includes system prompt + full cart contents. For large carts (50+ items), this can double. Cap the context window in the prompt or truncate cart contents to the top-N items to bound input cost.
