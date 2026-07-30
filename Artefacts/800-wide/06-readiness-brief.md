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
| 2 | **Who gets paged?** | Alert fires on `kube_pod_container_status_restarts_total > 3` in 5 min (Prometheus) or PagerDuty "cart-api OOMKilled". Oncall rotation: **`cart-api-oncall` PagerDuty schedule — primary owner must be named before go-live** (template below). | ⚠️ Rotation name needed |
| 3 | **What is monitored?** | Observability stack watches all layers: LB, cart-api pods, Redis, Postgres, DIAL gateway (latency, errors, cost). Known configured alerts: pod restarts > 3/5 min; AI spend alert at $12,000/month. Latency SLO (p99) and error-rate threshold → **UNKNOWN — owner needed** | ⚠️ SLO targets needed |
| 4 | **What does it cost per month, and what is the cap?** | $16,500/month: $1,500 cloud rent (flat) + $15,000 AI meter (3M calls × 1,400 tokens avg × blended rate). DIAL hard cap $16,000/month; alert at $12,000/month. Cap rejects calls with HTTP 429 on breach — does not silently swallow. | ✅ Documented (8.W.5) |
| 5 | **What is the kill-switch?** | (a) Deploy kill-switch: `kubectl rollout undo deployment/cart-api` — one command, <2 min to healthy. (b) AI meter kill-switch: DIAL hard cap at $16,000/month — gateway rejects summarise calls, cart checkout continues without the AI step. | ✅ Documented (8.W.2, 8.W.4, 8.W.5) |
| 6 | **Which support tier owns the top two ticket types?** | See L1–L3 handover table below. | ✅ Playbook written |

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
| **OOMKilled / CrashLoopBackOff** | **L1** — detect, escalate within 5 min | See L1 triage card below |
| | **L2** — owns recovery | `kubectl rollout undo` + confirm readinessProbe working + bump `limits.memory` in manifest; runbook: 8.W.4 |
| | **L3** — owns root-cause | RSS profiling, streaming fix, code change; escalate from L2 if rollback does not clear the loop or if non-summarise pods crash |
| **AI cost overage / DIAL 429 in production** | **L1** — detect, escalate within 5 min | See L1 triage card below |
| | **L2** — owns immediate response | Check DIAL dashboard for loop or batch spike; verify hard cap fired correctly; roll back the feature if call rate is anomalous |
| | **L3** — owns root-cause | Audit call volume by endpoint; implement streaming or per-request token budget; re-estimate cost model |

### L1 triage card — cart-api

> Execute in order. Total time budget: 5 minutes. Escalate to L2 with the event dump at step 3 if unresolved.

**Ticket type A — OOMKilled / CrashLoopBackOff**

```
Step 1 — Confirm scope (30 s)
  kubectl get pods -l app=cart-api
  → if STATUS = CrashLoopBackOff on ≥1 pod: continue
  → if all pods Running: close ticket, false alarm

Step 2 — Capture evidence (60 s)
  kubectl get events --field-selector reason=OOMKilling -n default \
    --sort-by=.lastTimestamp > /tmp/cart-api-events.txt
  kubectl describe pod -l app=cart-api | grep -A3 "Limits:" >> /tmp/cart-api-events.txt

Step 3 — Escalate to L2 (if pods still crashing after step 1)
  Page cart-api-oncall L2 via PagerDuty
  Attach /tmp/cart-api-events.txt
  State: "cart-api CrashLoopBackOff confirmed, OOMKill events present, limits output attached"
  Do NOT attempt kubectl rollout undo — that is an L2 action
```

**Ticket type B — AI cost overage / DIAL 429 errors**

```
Step 1 — Confirm scope (30 s)
  Check DIAL gateway dashboard for cart-api spend gauge
  Check error log for HTTP 429 responses from DIAL endpoint

Step 2 — Capture evidence (60 s)
  Note current spend-to-date and call rate from DIAL dashboard
  Screenshot or copy the gauge value

Step 3 — Escalate to L2
  Page cart-api-oncall L2 via PagerDuty
  State: "DIAL 429s observed / spend gauge at $X — possible loop or cap breach"
  Do NOT disable the cap — L2 decision
```

### Oncall rotation template

> Fill in before go-live. One named human must own the primary slot.

```yaml
# PagerDuty service: cart-api-oncall
escalation_policy:
  - level: 1
    responder: "[TEAM NAME] — primary on-call"   # ← fill in
    timeout_minutes: 5
  - level: 2
    responder: "[TEAM LEAD NAME]"                # ← fill in
    timeout_minutes: 10
  - level: 3
    responder: "[ENGINEERING MANAGER]"           # ← fill in
test_required: true   # fire end-to-end PagerDuty test to a real phone before go-live
```

---

## Maturity gap

| Gap | Severity | Status | Action needed |
|-----|----------|--------|--------------|
| Oncall rotation — names not filled in | **Blocker** | Template written, names blank | Fill in the three escalation slots in the oncall rotation template above; run PagerDuty end-to-end test to a real phone before go-live |
| Latency SLO (p99) and error-rate threshold | Medium | Not in artefacts | Set p99 target (suggested: 500 ms at p99) and error-rate alert (suggested: >1% 5xx over 5 min); export Prometheus rules |
| Secrets backend — Vault vs Sealed Secrets | Medium | Manifest says "in production" but not confirmed | Confirm which system is live and who owns key rotation schedule |

---

## Verdict

**Not ready to operate — one blocker remaining.**

Deploy path, rollback, cost cap, top failure runbook, L1 triage card, and L2/L3 handover are all documented. The single remaining blocker: the oncall rotation template is written but the three name slots are blank. Until a named human is in slot 1, a P1 page has no guaranteed recipient.

**One action to unblock:** fill in the escalation policy names above and verify a PagerDuty end-to-end test fires to a real phone before the deploy window. Once done, status moves to **Ready for monitored go-live**.
