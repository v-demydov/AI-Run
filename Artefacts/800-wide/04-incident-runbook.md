---
kata: 8.W.4
date: 2026-07-30
service: cart-api
incident: OOMKilled CrashLoopBackOff after deploy adding AI summarise step
severity: P1 — error rate climbing, healthy pods absorbing load
---

# Incident Runbook — cart-api OOMKilled

## Incident brief

Half of `cart-api` pods in `CrashLoopBackOff`. Events show `OOMKilled`.
Crash started **20 minutes** after a deploy that added the AI summarise step.
Error rate climbing; latency rising on healthy pods as they absorb the load
(readinessProbe keeps crashed pods out of rotation — Kata 8.W.2 fix working).

---

## Step 1 — Three ranked hypotheses

### H1 — No memory limit (or too-low limit) + AI summarise step is memory-hungry ★ most likely

**Evidence:**
- OOMKilled is a kernel hard kill: the process exceeded the container memory limit (or the node limit if no `resources.limits` is set).
- The crash started exactly after the deploy that added the AI step — timing is causal, not coincidental.
- The Kata 8.W.2 audit found `resources.limits` absent from the first-draft manifest. If that gap was not closed before this deploy, the pods have no ceiling and any memory spike evicts them.
- The AI summarise step buffers the full LLM response in memory. At ~3M calls/month (≈2 req/s average, bursty), each request holding a large completion string can spike per-pod RSS by 50–200 MB depending on response size and whether responses are streamed or buffered.

**Cheapest confirming step:**
```bash
kubectl describe pod $(kubectl get pods -l app=cart-api \
  --field-selector=status.phase=Running -o name | head -1) \
  | grep -A5 "Limits\|OOMKilled\|Last State"
```
If `Limits: <none>` or `memory: 256Mi` (requests-only, no limits) → H1 confirmed.

---

### H2 — Memory limit set correctly but per-request buffering causes spike ★★ second

**Evidence:**
- If limits were added post-audit but set to the old baseline (512Mi) without accounting for the AI step's working memory, pods are within limits until summarise calls arrive, then spike past them.
- The 20-minute lag could reflect the time for summarise traffic to warm up after deploy (cold-start, cache miss, first real user batch).

**Cheapest confirming step:**
```bash
kubectl top pods -l app=cart-api --sort-by=memory
```
If surviving pods are at 90–100% of their limit and growing → H2 confirmed; limit is too low, not absent.

---

### H3 — Memory leak introduced in the new code path ★ least likely initially

**Evidence:**
- OOMKilled after a new feature deploy can indicate a leak (response objects not released, connection pool not bounded).
- However: a leak shows gradual RSS growth over minutes to hours, not a hard crash 20 minutes after deploy. The pattern here (sudden, half the fleet, new AI step) points to a ceiling hit, not a slow climb.
- Worth keeping as H3 if H1 and H2 are ruled out and pods that did not serve summarise calls are also crashing.

**Cheapest confirming step:**
```bash
kubectl logs <pod> --previous | tail -50
```
Look for `heap out of memory`, Python `MemoryError`, or connection-pool exhaustion messages before the OOMKill — a leak leaves traces; a hard ceiling hit does not.

---

## Step 2 — Cheapest first action (settles H1 vs H2 in 60 seconds)

```bash
# 1. Check limits on a running pod
kubectl describe pod -l app=cart-api | grep -A 3 "Limits:"

# 2. Check recent OOMKill reason on a dead pod
kubectl get events --field-selector reason=OOMKilling -n default --sort-by=.lastTimestamp
```

**Decision tree:**
- `Limits: <none>` → H1. Immediate mitigation: rollback + set limits.
- `Limits: memory 512Mi` + pod at 490Mi → H2. Immediate mitigation: rollback + raise limit.
- Neither → run H3 log check.

---

## Step 3 — Immediate mitigation and durable fix

### Immediate mitigation (L2, ~2 minutes)

Roll back the deploy. The CI pipeline from Kata 8.W.3 makes this one command:

```bash
kubectl rollout undo deployment/cart-api
kubectl rollout status deployment/cart-api --timeout=60s
```

Healthy pods restart, traffic distributes, error rate drops. This does **not** fix the root cause — it restores service while the fix is prepared.

### Durable fix (L2/L3, same day)

1. **Profile the summarise step** — measure peak RSS during an AI call:
   ```python
   # in test/benchmark_summarise.py
   import tracemalloc
   tracemalloc.start()
   # ... call summarise endpoint ...
   current, peak = tracemalloc.get_traced_memory()
   print(f"peak: {peak / 1e6:.1f} MB")
   ```

2. **Set resource limits based on measurement**, not the old baseline:
   ```yaml
   resources:
     requests:
       memory: "512Mi"
       cpu: "200m"
     limits:
       memory: "1Gi"      # headroom above measured peak
       cpu: "1000m"
   ```

3. **Stream the LLM response** instead of buffering the full completion — reduces peak per-request RSS from O(response_size) to O(chunk_size).

4. **Re-deploy through CI** (Kata 8.W.3 pipeline) so the rollback gate confirms pods are healthy before the workflow succeeds.

---

## Runbook entry (reusable)

| Field | Content |
|-------|---------|
| **Detection signal** | Alert: `kube_pod_container_status_restarts_total > 3` in 5 min, OR PagerDuty page "cart-api OOMKilled", OR `kubectl get events --field-selector reason=OOMKilling` shows entries for `cart-api` pods |
| **Diagnosis steps** | 1. `kubectl describe pod -l app=cart-api \| grep -A3 "Limits:"` — confirm limit present/absent. 2. `kubectl top pods -l app=cart-api` — check memory pressure on surviving pods. 3. `kubectl get events --sort-by=.lastTimestamp` — confirm OOMKill, note timing vs last deploy. 4. `kubectl rollout history deployment/cart-api` — identify the deploy that preceded the crash |
| **Fix** | **If limits absent or too low:** (a) rollback immediately (`kubectl rollout undo deployment/cart-api`); (b) profile the new code path for peak RSS; (c) set `resources.limits.memory` to measured peak + 30% headroom; (d) re-deploy via CI — pipeline rollout gate must pass before closing incident |
| **Rollback** | `kubectl rollout undo deployment/cart-api && kubectl rollout status deployment/cart-api --timeout=60s`. Verify error rate drops within 2 minutes. If not, check readinessProbe is configured (Kata 8.W.2) — without it, the rolled-back pods may not re-enter rotation. |
| **Owning tier** | **L2 owns recovery** (rollback + limit bump in manifest). **L3 owns root-cause** (profiling, streaming fix, code change). Escalate to L3 if rollback does not clear the CrashLoopBackOff, or if pods without summarise traffic are also crashing (points to H3 memory leak). |

---

## What the Kata 8.W.2 gap cost

The missing `resources.limits` was flagged in the manifest audit. The cost of shipping without it:
- ~20 minutes of degraded service (50% pod loss)
- Healthy pods at elevated latency absorbing 2× load
- P1 incident, 2 a.m. page

The durable fix takes one YAML block. The runbook above makes the next occurrence an L2 resolution in under 10 minutes.
