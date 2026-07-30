---
kata: 8.W.6
date: 2026-07-30
service: cart-api
sources: 01-stack-map · 02-deploy-manifest · 03-ci-workflow · 04-incident-runbook · 05-cost-estimate
---

# Cloud Operations & Support Pack — cart-api

_One-page readout for security and delivery leads. Two minutes to read._

---

## Six readiness questions

| # | Question | Answer | Status |
|---|----------|--------|--------|
| 1 | **How does it deploy and roll back?** | Push to `main` → GitHub Actions pipeline: test → Trivy CVE scan → cosign image sign → `k8s-deploy` → `kubectl rollout status` rollback gate. Rollback: `kubectl rollout undo deployment/cart-api` (restores previous pinned image in <2 min, readinessProbe keeps bad pods out of rotation). | ✅ Documented (8.W.3) |
| 2 | **Who gets paged?** | Alert fires on `kube_pod_container_status_restarts_total > 3` in 5 min (Prometheus) or PagerDuty "cart-api OOMKilled". Oncall rotation owner and escalation path → **UNKNOWN — owner needed** | ⚠️ Partial |
| 3 | **What is monitored?** | Observability stack watches all layers: LB, cart-api pods, Redis, Postgres, DIAL gateway (latency, errors, cost). Known configured alerts: pod restarts > 3/5 min; AI spend alert at $12,000/month. Full alert inventory (latency SLO, error-rate threshold) → **UNKNOWN — owner needed** | ⚠️ Partial |
| 4 | **What does it cost per month, and what is the cap?** | $16,500/month: $1,500 cloud rent (flat) + $15,000 AI meter (3M calls × 1,400 tokens avg × blended rate). DIAL hard cap $16,000/month; alert at $12,000/month. Cap rejects calls with HTTP 429 on breach — does not silently swallow. | ✅ Documented (8.W.5) |
| 5 | **What is the kill-switch?** | (a) Deploy kill-switch: `kubectl rollout undo deployment/cart-api` — one command, <2 min to healthy. (b) AI meter kill-switch: DIAL hard cap at $16,000/month — gateway rejects summarise calls, cart checkout continues without the AI step. | ✅ Documented (8.W.2, 8.W.4, 8.W.5) |
| 6 | **Which support tier owns the top two ticket types?** | See L1–L3 handover table below. | ⚠️ L1 gap |

---

## Top failure and runbook

**Top failure: OOMKilled CrashLoopBackOff after AI-feature deploy** (P1, seen in practice)

| Step | Action | Time |
|------|--------|------|
| Detect | `kubectl get events --field-selector reason=OOMKilling` or PagerDuty page | T+0 |
| Triage | `kubectl describe pod -l app=cart-api \| grep -A3 "Limits:"` — absent or too-low limit confirms cause | T+1 min |
| Mitigate | `kubectl rollout undo deployment/cart-api` → `kubectl rollout status --timeout=60s` — verify error rate drops | T+3 min |
| Root-cause | Profile peak RSS with `tracemalloc`; set `resources.limits.memory` to measured peak + 30%; stream LLM response | same day |

Full runbook: `Artefacts/800-wide/04-incident-runbook.md`

---

## L1–L3 support handover

| Ticket type | Tier | Playbook |
|-------------|------|---------|
| **OOMKilled / CrashLoopBackOff** | **L1** — detect, escalate if not resolved in 5 min | Alert triage only; no L1 playbook exists yet → **UNKNOWN — owner needed** |
| | **L2** — owns recovery | `kubectl rollout undo` + confirm readinessProbe working + bump `limits.memory` in manifest; runbook: 8.W.4 |
| | **L3** — owns root-cause | RSS profiling, streaming fix, code change; escalate from L2 if rollback does not clear the loop or if non-summarise pods crash |
| **AI cost overage / DIAL 429 in production** | **L2** — owns immediate response | Check DIAL dashboard for loop or batch spike; verify hard cap fired correctly; roll back the feature if call rate is anomalous |
| | **L3** — owns root-cause | Audit call volume by endpoint; implement streaming or per-request token budget; re-estimate cost model |

---

## Maturity gap

| Gap | Severity | Action needed |
|-----|----------|--------------|
| Oncall rotation unassigned | **Blocker** | Name a team and on-call rotation before go-live; PagerDuty alert exists but has no verified recipient |
| L1 playbook absent | High | Write a 3-step L1 triage card (check pod status, check events, escalate to L2 with event dump) |
| Full alert inventory not documented | Medium | Export Prometheus alert rules; confirm latency SLO (p99 target) and error-rate threshold are configured |
| Secrets backend not confirmed | Medium | Manifest references Vault / Sealed Secrets "in production" — confirm which system is live and who owns rotation |

---

## Verdict

**Not ready to operate without mitigation. One blocker.**

The deploy path, rollback, cost cap, and top failure runbook are all documented and tested. The single blocker is an unassigned oncall rotation: the PagerDuty alert fires but no named human or team is confirmed as the recipient. Until that is resolved, the first P1 incident has no guaranteed responder. All other gaps (L1 playbook, alert inventory, secrets backend) are high-priority but non-blocking for a monitored soft launch.

**One action to unblock:** name the oncall rotation owner and verify a PagerDuty end-to-end test fires to a real phone before the deploy window.
