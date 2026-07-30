---
kata: K8.3
date: 2026-07-30
service: cart-api
source: Artefacts/800-wide/05-cost-estimate.md
ceiling: $16,500/month
dial_hard_cap: $16,000/month
alert_threshold: $12,000/month
---

# AI Cost Estimate — cart-api (agent summary)

_Extracted and verified from `Artefacts/800-wide/05-cost-estimate.md`._

## Line-by-line arithmetic

| Line | Calculation | Result |
|------|-------------|--------|
| Input tokens/month | 3,000,000 calls × 1,200 tokens/call | 3,600 M tokens |
| Input cost | 3,600 M × $2.50/M | **$9,000** |
| Output tokens/month | 3,000,000 calls × 200 tokens/call | 600 M tokens |
| Output cost | 600 M × $10.00/M | **$6,000** |
| **AI meter subtotal** | | **$15,000/month** |
| Cloud rent (flat) | 3 pods + Postgres + Redis + LB | **$1,500/month** |
| **Monthly total** | | **$16,500/month** |

Hand-check: 3,000,000 × 1,200 × $2.50 / 1,000,000 = $9,000 input alone. Confirmed.

## Split

| Bucket | Amount | Share | Owner |
|--------|--------|-------|-------|
| Cloud rent (flat) | $1,500 | 9% | Platform / Ops |
| AI meter (variable) | $15,000 | 91% | **Cart product team** |

## Ceiling and cap

| Threshold | Value | Meaning |
|-----------|-------|---------|
| Monthly total ceiling | $16,500 | Current run-rate; any change exceeding this requires cart team approval |
| DIAL hard cap | $16,000/month | Gateway rejects AI calls with HTTP 429 on breach — checkout continues, summarise step fails gracefully |
| DIAL alert | $12,000/month | Fires at 80% of cap — investigation window before production impact |

## Status: within ceiling

At current volume (3M calls/month), the AI meter is $15,000 — $1,000 below the DIAL hard cap. No action required today.

## When this estimate must be re-run

- Any deploy that changes call volume (batch jobs, new endpoints calling summarise)
- Any deploy that changes token budget per call (larger system prompt, unbounded cart content)
- Before approving a DIAL cost-cap raise
