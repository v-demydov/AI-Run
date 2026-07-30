---
kata: K8.3
date: 2026-07-30
service: cart-api
pod: cart-api-7d9f8b-k2pqr
signal: OOMKilled CrashLoopBackOff (restart count: 4)
inputs: cluster-state/failure-A/describe.txt + logs.txt
slo_impact: ~20 min downtime = 46% of 43.8-min monthly error budget consumed
---

# Pod Diagnosis — cart-api OOMKilled

## Signal summary

| Field | Value |
|-------|-------|
| Pod state | CrashLoopBackOff |
| Last termination reason | OOMKilled (exit code 137) |
| Restart count | 4 |
| Time from deploy to first crash | ~20 min (deploy added AI summarise feature) |
| Memory limits | `<none>` — confirmed in describe output |
| Liveness probe | `<none>` |
| Readiness probe | `<none>` |
| Image tag | `cart-api:latest` (floating — non-deterministic rollback) |
| Secrets in env | DATABASE_URL and DIAL_API_KEY as plaintext values |

---

## Three ranked hypotheses

### H1 — No memory limit; AI summarise step spikes RSS above node ceiling   **confidence: HIGH**

**Evidence:**
- `Limits: <none>` explicit in `describe.txt` line 29–30. Without a limit, the kernel OOM killer fires when the pod's RSS exceeds node-level pressure — there is no container-level ceiling to trigger a graceful restart first.
- Exit code 137 = SIGKILL from the kernel OOM killer. This is a hard kill, not a graceful shutdown.
- All 21 logged requests are `/cart/xxx/summarise`. Each buffers a full LLM response in memory (~195–235 output tokens = ~1–2 KB per response, but the in-flight Python object overhead is larger — typically 50–200 MB per concurrent request depending on context size).
- The `requests.memory: 256Mi` value sets the *scheduling* floor, not a runtime ceiling. The process can grow well past it.
- The Kata 8.W.2 manifest audit identified `resources.limits` absent as gap #1.

**Read-only confirmation command:**
```bash
kubectl describe pod -l app=cart-api | grep -A3 "Limits:"
```
Expected output confirming H1: `Limits: <none>` on all running pods. If any pod shows `memory: NNNMi`, move to H2.

---

### H2 — Memory limit set but too low for the AI step's working memory   **confidence: MEDIUM**

**Evidence:**
- If `resources.limits` was added post-8.W.2 audit but sized to the old baseline (512 Mi or lower) without accounting for the summarise step's working memory, pods stay within limits under normal cart traffic but spike past them when summarise calls arrive concurrently.
- The 20-minute lag between deploy and first crash is consistent with H2: the pod starts healthy under low traffic, then the first burst of summarise requests pushes it past the limit.
- Log token counts in the final 10 minutes are trending upward (input: 1,199 → 1,421; output: 199 → 235), suggesting larger cart payloads arriving in the last phase — consistent with a per-request size trigger rather than a slow leak.

**Read-only confirmation command:**
```bash
kubectl top pods -l app=cart-api --sort-by=memory
```
Expected output confirming H2: surviving pods at 85–100% of their configured limit and growing. If `<none>`, H1 is confirmed instead.

---

### H3 — Memory leak in the new summarise code path   **confidence: LOW**

**Evidence:**
- OOMKilled after a feature deploy can indicate a leak (response objects not GC'd, connection pool unbounded, LLM client holding references).
- The 20-minute lag is consistent with a slow-accumulating leak.

**Counter-evidence:**
- Logs show clean request/response pairs with no pre-crash memory warning lines — a Python leak typically surfaces with heap warnings or `MemoryError` before the hard kill.
- The hard stop with no final log line is more consistent with a ceiling hit (H1/H2) than a slow climb.
- There is no evidence that pods *not* serving summarise calls are also crashing; if they were, H3 would move to high confidence.

**Read-only confirmation command:**
```bash
kubectl logs cart-api-7d9f8b-k2pqr --previous | grep -iE "memory|heap|leak|traceback|MemoryError" | tail -30
```
Expected output confirming H3: repeated memory-pressure warnings climbing before the final entry. A clean log with abrupt end → H1 or H2.

---

## Recommended next step (read-only)

Run the H1 confirmation command first — it settles the diagnosis in 60 seconds:

```bash
kubectl describe pod -l app=cart-api | grep -A3 "Limits:"
```

**Decision tree:**
- `Limits: <none>` → H1 confirmed. Escalate to L2: rollback + set `resources.limits.memory: 1Gi`.
- `Limits: memory NNNMi` + surviving pod at 90%+ → H2 confirmed. Escalate to L2: rollback + raise limit.
- Neither → run H3 log check. Escalate to L3 if non-summarise pods are also crashing.

---

## Escalation

**This agent proposes the diagnosis. All write actions are human-owned.**

- `kubectl rollout undo deployment/cart-api` → L2 on-call (runbook: `Artefacts/800-wide/04-incident-runbook.md`)
- Setting `resources.limits.memory` → L2 manifest change via PR
- Profiling and streaming fix → L3 (Artefacts/800-wide/04-incident-runbook.md, Step 3 durable fix)

---

## SLO impact

This incident consumed ~20 minutes of availability downtime — 46% of the 43.8-minute monthly error budget defined in `slo/slo.md`. A recurrence before month-end would exhaust the budget entirely.
