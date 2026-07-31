---
service: cart-api
date: 2026-07-31
dfd: 00-dfd.mmd
---

# Asset Inventory — cart-api

| # | Asset | Classification | Rank | Rationale |
|---|-------|---------------|------|-----------|
| 1 | **DIAL API key** (`DIAL_API_KEY`) | Credential | **HIGH** | A live key authorising unbounded LLM spend; leaked as plaintext env var in the first-draft manifest (8.W.2) and visible in `kubectl describe` output — a stolen key lets an attacker exhaust the $16,000/month DIAL cap or exfiltrate data via crafted prompts |
| 2 | **DATABASE_URL** (Postgres credential with password) | Credential | **HIGH** | Grants full read/write access to all orders, user records, and cart history; leaked as plaintext in the first-draft manifest and in the `describe.txt` seed — compromised = complete database dump |
| 3 | **Customer cart contents** (items, quantities, prices in transit to LLM) | PII / Business data | **HIGH** | Sent to a third-party LLM provider via DIAL on every summarise call (~3M/month); once outside Trust Boundary 2 we cannot guarantee data residency, retention, or that the provider does not train on it — GDPR Article 28 processor agreement required |
| 4 | **Postgres order and user records** (order history, cart history, user PII) | PII / Business data | **HIGH** | Full durable store of customer PII; a successful SQL injection or credential leak results in a GDPR-notifiable breach; the `DATABASE_URL` credential (asset 2) is the direct attack path |
| 5 | **Kubernetes Secrets** (`cart-api-secrets`) | Credential store | **HIGH** | Holds assets 1 and 2 in etcd; if etcd encryption at rest is not enabled (not confirmed in artefacts) the secrets are stored as base64 — effectively plaintext; a cluster admin misconfiguration exposes all credentials in one operation |
| 6 | **Redis cart cache** (active cart state, all sessions) | PII / Session data | **MEDIUM** | Contains every in-flight cart in real time; shorter-lived than Postgres but an attacker with Redis access can read all active sessions instantly; TTL limits exposure window |
| 7 | **Observability logs** | Operational data / PII risk | **MEDIUM** | Request logs include `/cart/xxx/summarise` paths with token counts; if the app logs cart payloads or LLM summaries, logs become a PII amplifier; the `describe.txt` seed showed `DATABASE_URL` and `DIAL_API_KEY` logged in pod env — logs must be scrubbed of credentials |
| 8 | **Deployment manifests and CI workflow** | Configuration / Supply chain | **MEDIUM** | Contain image tags, resource limits, and (in first-draft) plaintext credentials; a compromised CI pipeline (supply-chain attack via floating action tags — 8.W.3 finding) can push a malicious image that passes the rollback gate |
| 9 | **LLM-generated cart summaries** | Derived / Transient data | **LOW** | AI-generated text summarising cart contents; no standalone value if not stored; impact is low unless logged verbatim (at which point see asset 7) |
| 10 | **Aggregate metrics** (request rates, latency histograms, error rates) | Operational data | **LOW** | No PII; useful for capacity planning only; if exfiltrated an attacker learns traffic patterns but gains no direct access to data or credentials |

---

## Highest-impact attack paths (from the DFD)

| Path | Assets at risk | Trust boundary crossed |
|------|---------------|----------------------|
| Plaintext DIAL_API_KEY in pod env → `kubectl describe` or CI log scrape | Asset 1 (DIAL key) → unbounded spend + prompt injection | TB2 (application) |
| Plaintext DATABASE_URL in pod env → same vector | Asset 2 (DB credential) + Asset 4 (all Postgres data) | TB2 → TB3 |
| Cart contents sent to LLM → provider data retention | Asset 3 (cart PII) | TB2 → TB4 |
| CI supply-chain: floating action tag → malicious image | Assets 1, 2, 4, 5 | TB1 → TB2 |

---

## Source artefacts

- Stack map: `Artefacts/800-wide/01-stack-map.md`
- Manifest audit (8 gaps): `Artefacts/800-wide/02-deploy-manifest.md`
- CI supply-chain audit (6 gaps): `Artefacts/800-wide/03-ci-workflow.md`
- Incident seed (plaintext creds in describe): `cluster-state/failure-A/describe.txt`
