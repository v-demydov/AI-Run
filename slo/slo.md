---
service: cart-api
date: 2026-07-30
owner: cart product team
---

# Service Level Objectives — cart-api

| Indicator | Target | Measurement window | Alert threshold |
|-----------|--------|-------------------|-----------------|
| Latency — p99 | ≤ 500 ms | 5-minute rolling | p99 > 500 ms for > 2 min |
| Error rate (5xx) | < 1 % | 5-minute rolling | > 1 % 5xx for > 2 min |
| Availability | 99.9 % monthly | Calendar month | Pod restarts > 3 in 5 min |
| AI summarise p99 | ≤ 1,500 ms | 5-minute rolling | p99 > 1,500 ms for > 2 min |

## Error budget

99.9 % availability = 43.8 minutes downtime budget per month.

The OOMKilled incident (8.W.4) consumed approximately 20 minutes —
46 % of the monthly error budget in one event.

## SLO owner

Changes to these targets require sign-off from the cart product owner.
The ops team monitors and pages; the product team owns the bar.
