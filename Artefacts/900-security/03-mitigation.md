---
kata: 9.W.4
date: 2026-07-31
service: cart-api
top_critical_threat: T-07
---

# Mitigation Plan — T-07 (Top Critical Risk)

## Top-critical row (from 02-risks.csv)

| Field | Value |
|-------|-------|
| **Threat ID** | T-07 |
| **Element** | cart-api (Process) |
| **STRIDE** | Information Disclosure |
| **Likelihood** | High — confirmed happening today; env vars visible in `kubectl describe`; requires only observability read access |
| **Impact** | High — live DIAL_API_KEY + DATABASE_URL exposed to any developer with observability access |
| **Severity** | **Critical (H × H)** |
| **Blast radius** | DIAL_API_KEY: $16,000 cap breach in <1 hour of automated calls; ~3M customer cart sessions per month reachable via prompt injection; DATABASE_URL: full Postgres dump of all orders and user PII; credential visible to any of ~20 developers with observability read access |

---

## Three-class mitigation

### Preventive control — Stop the credential reaching the environment surface

**What it does:** Replace the plaintext `env.value` injection of `DIAL_API_KEY` and `DATABASE_URL` with `secretKeyRef` references to the `cart-api-secrets` Kubernetes Secret object (the fix already specified in `Artefacts/800-wide/02-deploy-manifest.md`). Add a manifest-linting gate in the GitHub Actions CI pipeline (`03-ci-workflow.md`) that rejects any PR containing a literal `DIAL_API_KEY` or a URL-password pattern in an `env.value` field — so a future revert of this fix is automatically blocked before merge.

**Threat property it closes:** Removes the root cause — the credential never enters the pod's environment as a visible string, so it cannot appear in `kubectl describe`, startup logs, or crash dumps.

**Why it matches Information Disclosure (STRIDE):** An Information Disclosure threat is best prevented at the source: if the secret is never rendered as plaintext in the environment, there is nothing to disclose. The `secretKeyRef` approach means the kubelet injects the value from the encrypted Secret store directly into the process environment without materialising it in the manifest, the pod spec, or any describe output.

| Field | Value |
|-------|-------|
| **Owner** | Lead Engineer, cart-api — **[NAME TO BE FILLED IN]** |
| **Deadline** | 2026-08-14 (14 days — no new deploy until this is merged and verified) |
| **Done when** | `kubectl describe pod -l app=cart-api \| grep DIAL_API_KEY` returns no value; CI pipeline rejects a test PR containing a plaintext key pattern |

---

### Detective control — Alert within 5 minutes if any credential pattern appears in logs

**What it does:** Deploy a Falco rule (or a log-aggregation regex in the observability stack) that fires a PagerDuty alert whenever the string pattern `sk-live-`, `DIAL_API_KEY`, or a Postgres URL password pattern (`postgres://.*:.*@`) appears in any cart-api log line, pod describe output scraped by the observability collector, or CI log artifact. Alert fires to the `cart-api-oncall` channel within 5 minutes of first match.

**Threat property it closes:** Reduces the time-to-detection window from "never" (current state — no alert exists) to ≤5 minutes, bounding the exposure window between a reintroduced plaintext credential and the rotation response (Responsive control below).

**Why it matches Information Disclosure (STRIDE):** When prevention fails or is bypassed (e.g. an emergency hotfix deployed without CI), the detective control is the only thing between a credential sitting in logs for days and a rapid response. Detection is the second line of defence specifically against passive disclosure threats where the damage accumulates silently over time.

| Field | Value |
|-------|-------|
| **Owner** | Platform/Ops Lead — **[NAME TO BE FILLED IN]** |
| **Deadline** | 2026-08-20 (20 days — Falco or log-scan rule deployed and end-to-end tested with a synthetic `sk-live-test` string) |
| **Done when** | Injecting `echo "DIAL_API_KEY=sk-live-test"` into a test pod log triggers a PagerDuty alert within 5 minutes |

---

### Responsive control — Credential rotation runbook, executable within 1 hour of detection

**What it does:** A documented, rehearsed runbook that an on-call engineer can execute within 1 hour of the detective control firing:
1. Issue a new DIAL API key via the DIAL gateway admin portal; update `cart-api-secrets`; rolling-restart cart-api pods (the 8.W.3 pipeline rollout gate confirms pods healthy before old key is invalidated).
2. Rotate the Postgres `cartdb` user password via the DBA runbook; update `cart-api-secrets`; rolling-restart.
3. Pull DIAL audit logs for the 30-day window preceding rotation; check for unauthorized `POST /v1/chat` calls from unknown source IPs; report to CISO if found.
4. Downgrade cart-api log level from DEBUG to INFO for all environments where DEBUG is confirmed; deploy via ConfigMap update (no image rebuild required).

**Threat property it closes:** Bounds the consequence window — even if the credential was read before the detective alert fired, rotating it within 1 hour limits the usable exposure to that window and eliminates ongoing risk.

**Why it matches Information Disclosure (STRIDE):** A responsive control for an Information Disclosure threat cannot un-disclose the information, but it can revoke the disclosed credential and contain downstream damage. The blast radius (T-07 note) scales directly with how long the credential remains valid after exposure — this runbook minimises that window.

| Field | Value |
|-------|-------|
| **Owner** | On-call Engineer (L2) following escalation from the detective alert — **[NAME: cart-api-oncall primary slot, see 06-readiness-brief.md oncall template]** |
| **Deadline** | Runbook written and rehearsed in a dry run by 2026-08-28 |
| **Done when** | Dry-run confirms credential rotation completes end-to-end in <1 hour with healthy pods at the end of the rollout gate |

---

## Residual-risk acceptance contract

After all three controls are implemented and verified, the following residual risk remains:

| Field | Content |
|-------|---------|
| **Risk statement** | **Cause:** A developer or insider with legitimate observability read access deliberately reads DIAL_API_KEY or DATABASE_URL from a log line or pod describe during the window between a new deployment and the next Falco scan cycle (up to 5 minutes). **Event:** The credential is used to make unauthorized DIAL calls or read Postgres data before the detective alert fires and rotation completes. **Consequence:** Up to 5 minutes × ~67 DIAL calls/minute = ~335 unauthorized LLM calls ($0.05 estimated cost); limited Postgres queries if the DATABASE_URL was also read. Reputational and GDPR notification risk if any customer PII was returned. |
| **Named owner** | **[Engineering Manager, cart-api team — NAME TO BE FILLED IN]** — this individual accepts the residual risk and is accountable for re-evaluation |
| **Expiry date** | 2026-08-30 — all three controls must be verified complete; if any are not, the residual risk escalates to unmitigated Critical and the deploy is blocked |
| **Re-evaluation triggers** | (1) Any new manifest PR that touches `env:` blocks; (2) DIAL_API_KEY pattern detected in a Falco alert (indicates the preventive control was bypassed); (3) Rotation of credentials outside this runbook (e.g. DIAL provider forces key change); (4) Any change to observability access roster (new developer granted read access); (5) DIAL provider publishes a security advisory |
| **Approver** | **[CISO or Security Lead — NAME TO BE FILLED IN]** — must sign before cart-api v1.5.0 re-enters production with the AI summarise feature enabled |

---

## Names required before this document is complete

This mitigation plan contains **4 named-individual placeholders** — `[NAME TO BE FILLED IN]`. Per the kata rule: a control without a named individual is not mitigated. The team must fill in:

1. Lead Engineer, cart-api (Preventive control owner)
2. Platform/Ops Lead (Detective control owner)
3. On-call primary slot holder (Responsive control owner — see `Artefacts/800-wide/06-readiness-brief.md` oncall rotation template)
4. Engineering Manager (Residual-risk owner) + CISO/Security Lead (Approver)

Until all four are named, the residual-risk contract is not executable and this risk remains **unmitigated Critical**.
