---
kata: K8.3
date: 2026-07-30
agent: ops-cart-api
scope: read-only triage + IaC audit + cost gating for cart-api
---

# Agent Bounds — ops-cart-api

_Seven runtime bounds. Each carries a number+unit. No prose bounds._

## Runtime bounds

| # | Bound | Value | Rationale |
|---|-------|-------|-----------|
| 1 | `retry_cap` | ≤ 2 retries per read operation | A kubectl describe or log fetch that fails twice indicates a cluster connectivity issue — escalate rather than retry indefinitely |
| 2 | `retry_cooldown` | ≥ 45 s between retries | Aligns with Kubernetes backoff window; avoids hammering the API server during an incident |
| 3 | `cost_cap_per_run` | ≤ $0.05 per session | Read-only operations (describe, logs, get, top) have near-zero AI token cost; any session exceeding $0.05 suggests an unexpected generative call — stop and alert |
| 4 | `max_read_ops_per_run` | ≤ 20 kubectl read operations | Bounds cluster API load during triage; if 20 reads are insufficient, the incident has outgrown automated triage — escalate to L3 |
| 5 | `max_hypotheses` | exactly 3 | No fewer (forces ranking), no more (forces prioritisation); a fourth hypothesis is a signal to escalate, not to expand the list |
| 6 | `escalation_timeout` | 5 min from first escalation signal | If the on-call human has not acknowledged within 5 min of a page, auto-page the next escalation tier (L2 → L3); do not wait indefinitely |
| 7 | `session_ttl` | ≤ 30 min per triage session | After 30 min without a human resolution decision, re-page and present a summary; stale sessions accumulate context that diverges from cluster reality |

## Kill-switch

| Method | Action | Owner |
|--------|--------|-------|
| Primary | Delete `.claude/skills/ops/skill.md` — the agent stops being invocable immediately | Any engineer with repo write access |
| Secondary | Revoke the DIAL API key used by the ops agent session — the agent can still read the cluster but cannot make AI-assisted calls | Platform / Ops team |
| Emergency | Both: delete the skill file AND revoke DIAL access | L3 on-call |

## What this agent may never do

| Never | Approval surface if needed |
|-------|---------------------------|
| `kubectl apply` / `delete` / `patch` / `exec` | PR review → CI pipeline → L2 approval |
| `terraform apply` | Signed change-management ticket → L3 approval |
| Gateway policy change (DIAL quota, rate limit) | Cart product team sign-off + ops ticket |
| `kubectl rollout undo` | L2 on-call decision (runbook: 8.W.4) |
| SLO target change | Cart product owner sign-off (slo/slo.md owner) |
| DIAL hard-cap raise | Cart product team P&L owner + ops confirmation |
| Page to on-call | Triggered by alert rule, not by this agent directly |

## Escalation path

```
ops-cart-api agent (read-only triage)
    │
    ├─ H1/H2 confirmed → page L2 on-call with event dump
    │       └─ L2: kubectl rollout undo + manifest PR
    │
    ├─ H3 suspected (non-summarise pods crashing) → page L3
    │       └─ L3: profiling + streaming fix + code change
    │
    ├─ IaC blocker found → block PR, notify PR author + L2 reviewer
    │
    └─ Cost estimate exceeds $16,000 cap → block deploy,
            notify cart product team P&L owner for cap-raise approval
```
