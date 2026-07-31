---
kata: 9.W.5
date: 2026-07-31
service: cart-api
control_path: 2 — Secrets scanner in CI
threat: T-07 (Information Disclosure — DIAL_API_KEY / DATABASE_URL in plaintext env.value)
commit_sha: 83390d8b482160ae0f61a4acca79c4ecc1067408
branch: security/9w5-secrets-scanner
---

# Evidence Pack — T-07 Preventive Control

---

## Block 1 — Control identity

| Field | Value |
|-------|-------|
| **Control name** | `check_k8s_secrets.py` — k8s manifest plaintext-credential scanner |
| **Control class** | Preventive (stops the credential reaching the merge queue) |
| **Framework mapping** | SOC 2 CC6.1 — Logical and physical access controls: "The entity implements logical access security measures to protect against threats from sources outside its system boundaries." ISO 27001 Annex A A.9.4.2 — Secure log-on procedures; A.10.1.1 — Policy on the use of cryptographic controls. |
| **Plain-language description** | A Python script that parses every Kubernetes YAML manifest and rejects any file where a container `env:` entry uses a literal `value:` for a known sensitive name (`DIAL_API_KEY`, `DATABASE_URL`, `DB_PASSWORD`, `API_KEY`, `SECRET_KEY`) or a known secret value pattern (`sk-live-*`, `postgres://user:pass@`). The script is wired into a GitHub Actions workflow (`security-scan.yml`) that runs on every PR touching a `.yaml` file and fails the workflow — blocking merge — if any finding is returned. |
| **Scope** | All `k8s/` manifests in the `cart-api` repository; any PR that changes a `.yaml` or `.yml` file |
| **Threat it closes** | T-07: plaintext `DIAL_API_KEY` and `DATABASE_URL` visible in pod env, `kubectl describe` output, and startup logs |
| **Residual-risk owner** | Engineering Manager, cart-api team — **[NAME TO BE FILLED IN]** (from `Artefacts/900-security/03-mitigation.md`) |

---

## Block 2 — Test method

### Bypass-case test (the attack the control must block)

**Test input:** `tests/fixtures/bad-manifest.yaml` — a Deployment manifest with both `DIAL_API_KEY` and `DATABASE_URL` injected as plaintext `env.value` fields, matching the exact pattern found in the failure-A incident seed (`cluster-state/failure-A/describe.txt`).

**Test command:**
```bash
python3 scripts/check_k8s_secrets.py tests/fixtures/bad-manifest.yaml
```

**Actual output (captured 2026-07-31):**
```
FAIL: plaintext credentials detected in k8s manifests
  tests/fixtures/bad-manifest.yaml: env 'DIAL_API_KEY' uses plaintext value: — use secretKeyRef
  tests/fixtures/bad-manifest.yaml: env 'DIAL_API_KEY' value matches forbidden pattern (sk-live-)
  tests/fixtures/bad-manifest.yaml: env 'DATABASE_URL' uses plaintext value: — use secretKeyRef
  tests/fixtures/bad-manifest.yaml: env 'DATABASE_URL' value matches forbidden pattern (postgres://[^:]+:[^@]+@)

Fix: use secretKeyRef (see Artefacts/800-wide/02-deploy-manifest.md)
```

**Exit code:** `1` (workflow fails, merge blocked)

### Happy-path test (correct secretKeyRef usage must pass)

**Test command:**
```bash
python3 scripts/check_k8s_secrets.py tests/fixtures/good-manifest.yaml
```

**Actual output:**
```
PASS: no plaintext credentials found in 1 file(s)
```

**Exit code:** `0`

| Field | Value |
|-------|-------|
| **Commit SHA** | `83390d8b482160ae0f61a4acca79c4ecc1067408` |
| **Branch** | `security/9w5-secrets-scanner` |
| **Test date** | 2026-07-31 |
| **Test runner** | Local — `python3 scripts/check_k8s_secrets.py` |
| **CI workflow** | `.github/workflows/security-scan.yml` (triggers on PR; not yet run in GitHub Actions — see monitoring block) |

---

## Block 3 — Monitoring (design intent)

_Labelled "design intent" — the CI workflow is committed but no GitHub Actions run has completed yet. No weekly review cycle has run._

| Signal | Threshold | Action | Owner |
|--------|-----------|--------|-------|
| GitHub Actions workflow `security-scan / manifest-secrets-scan` fails on a PR | Any failure | PR is blocked from merge; PR author is notified by GitHub; security champion reviews within 1 business day | Lead Engineer, cart-api (**[NAME]**) |
| CI scan job exits 0 but a credential pattern appears in `kubectl describe` output (detected by Falco rule — see 03-mitigation.md Detective control) | Any match of `sk-live-` or `postgres://.*:.*@` in any pod log line | PagerDuty alert fires to `cart-api-oncall`; L2 initiates credential rotation runbook (03-mitigation.md Responsive control) | Platform/Ops Lead (**[NAME]**) |
| Weekly PR scan coverage review | Any week where fewer than 100% of merged PRs ran `security-scan` | Investigate CI bypass; escalate to Security Lead | Security Lead (**[NAME]**) |

**Design target (not yet implemented):** the weekly coverage review and the Falco rule are described in `03-mitigation.md` but no tooling has been deployed. The CI gate is the only currently active control.

---

## Block 4 — Audit trail

| Field | Value |
|-------|-------|
| **Log location** | GitHub Actions run logs for workflow `security-scan`; accessible at `https://github.com/<org>/cart-api/actions/workflows/security-scan.yml` |
| **Retention period** | GitHub Actions logs: 90 days by default (GitHub Enterprise: configurable up to 400 days). **Legal basis:** operational security log retention for audit trail integrity (GDPR Art. 5(1)(e) storage limitation; SOC 2 CC7.2 system monitoring). |
| **Immutability** | GitHub Actions logs are written by the GitHub runner and cannot be edited by repository contributors. Branch protection rules (`main` requires passing status checks) prevent force-push deletion of the run record. For this kata: "none — kata artifact"; no WORM storage is configured. |
| **Access control** | GitHub repository `read` access required to view workflow run logs. Secrets (`REGISTRY_USER`, `REGISTRY_PASSWORD` in the production workflow) are scoped to the repository and not exposed in logs. The scanner script itself contains no secrets. |
| **Test fixture retention** | `tests/fixtures/bad-manifest.yaml` is committed to the branch `security/9w5-secrets-scanner` as a permanent test artifact. It contains synthetic credentials matching the incident seed (not production values). |
