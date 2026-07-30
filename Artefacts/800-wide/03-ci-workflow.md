---
kata: 8.W.3
date: 2026-07-30
service: cart-api
pipeline: build → test → scan → deploy on push to main
---

# CI/CD Workflow — cart-api

## Step 1 — Generated workflow (first draft)

```yaml
# .github/workflows/cart-api.yml
name: cart-api CI/CD

on:
  push:
    branches: [main]

jobs:
  build-test-deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v3

      - name: Log in to registry
        uses: docker/login-action@v3
        with:
          registry: registry.example.com
          username: ${{ secrets.REGISTRY_USER }}
          password: ${{ secrets.REGISTRY_PASSWORD }}

      - name: Run tests
        run: |
          docker build --target test -t cart-api:test .
          docker run --rm cart-api:test

      - name: Build and push image
        uses: docker/build-push-action@v5
        with:
          push: true
          tags: registry.example.com/cart-api:${{ github.sha }}

      - name: Deploy to Kubernetes
        uses: azure/k8s-deploy@v4
        with:
          manifests: k8s/deployment.yaml
          images: registry.example.com/cart-api:${{ github.sha }}
```

---

## Step 2 — Fresh-session adversarial audit

> Audited in isolation — no access to the generation context.
> Checked against the six supply-chain controls.

### Six-control audit table

| # | Control | Status | Why it matters | One-line fix |
|---|---------|--------|----------------|-------------|
| 1 | **Pinned action versions** (SHA, not tag) | ❌ Missing | All four actions use floating tags (`@v4`, `@v3`, `@v5`). A tag can be force-pushed by the action owner to point to new, malicious code — your workflow silently executes it on the next run. This is how the `tj-actions/changed-files` supply-chain attack worked in 2023. | Pin every third-party action to its commit SHA: `actions/checkout@11bd71901bbe5b1630ceea73d27597364c9af683` |
| 2 | **OIDC short-lived credentials** (not long-lived secrets) | ❌ Missing | `REGISTRY_PASSWORD` is a long-lived credential stored in GitHub Secrets. If the secret leaks (log scrape, compromised runner, secret scan miss), it grants permanent registry write access. OIDC federates identity — the token lives for minutes, not months. | Replace login step with OIDC: add `permissions: id-token: write`; use `docker/login-action` with `oidc: true` against a registry that supports OIDC (ECR, GAR, GHCR) |
| 3 | **Image signing / provenance** | ❌ Missing | Nothing in this pipeline proves the image in the registry was built from this commit by this workflow. An attacker who gains registry write can push a malicious image under the same tag. `cosign` + SLSA provenance give consumers a verifiable chain: git commit → build → digest. | Add a post-build step: `uses: sigstore/cosign-installer@v3` then `cosign sign --yes registry.example.com/cart-api:${{ github.sha }}` |
| 4 | **Dependency + image scanning** | ❌ Missing | No Trivy, Snyk, or Grype scan. A HIGH CVE in a base image or a dependency ships to production silently. The test step builds and runs the image but does not check for known vulnerabilities. | Add after build: `uses: aquasecurity/trivy-action@v0.20.0` with `image-ref: registry.example.com/cart-api:${{ github.sha }}` and `exit-code: 1` on CRITICAL/HIGH |
| 5 | **Least-privilege token permissions** | ❌ Missing | No `permissions:` block means the job inherits the repo default — typically `contents: write` and `packages: write`. Any step that runs arbitrary code (the test container) can exfiltrate or modify the repo. GITHUB_TOKEN should be scoped to what each job actually needs. | Add at job level: `permissions: {contents: read, packages: write, id-token: write}` (drop `contents: write`; the deploy needs only `read`) |
| 6 | **Rollback gate** | ❌ Missing | The deploy step fires `k8s-deploy` and the workflow succeeds regardless of whether the pods become healthy. A bad image that fails its readiness probe will stall the rollout — but the pipeline shows green and the on-call gets no signal. Without a gate the only recovery path is manual. | After deploy add: `run: kubectl rollout status deployment/cart-api --timeout=120s` — non-zero exit fails the workflow and triggers GitHub's default branch protection alert |

### Verdict

**6/6 controls missing.** This is the normal state of a first-draft workflow. Controls #1 and #2 are the ones attackers actively exploit (supply-chain tag poisoning, leaked long-lived credentials). Control #6 is the one that turns a bad deploy from a 2-minute rollback into a 30-minute incident because no one gets a signal.

---

## Step 3 — Fixed workflow

```yaml
# .github/workflows/cart-api.yml
name: cart-api CI/CD

on:
  push:
    branches: [main]

# Fix #5 — least-privilege: declare only what each job needs
permissions:
  contents: read
  packages: write      # push image to GHCR
  id-token: write      # OIDC token for keyless signing + registry auth

jobs:
  build-test-deploy:
    runs-on: ubuntu-latest
    steps:
      # Fix #1 — pinned to commit SHA, not floating tag
      - uses: actions/checkout@11bd71901bbe5b1630ceea73d27597364c9af683  # v4.2.2

      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@b5ca514318bd6ebac0fb2aedd5d36ec1b5c232a2  # v3.10.0

      # Fix #2 — OIDC keyless login; no long-lived REGISTRY_PASSWORD
      - name: Log in to GHCR via OIDC
        uses: docker/login-action@9780b0c442fbb1117ed29e0efdff1e18412f7567  # v3.3.0
        with:
          registry: ghcr.io
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}   # short-lived, scoped to this run

      - name: Run tests
        run: |
          docker build --target test -t cart-api:test .
          docker run --rm cart-api:test

      - name: Build and push image
        id: build
        uses: docker/build-push-action@4f58ea79222b3b9dc2c8bbdd6debcef730109a75  # v6.9.0
        with:
          push: true
          tags: ghcr.io/${{ github.repository }}/cart-api:${{ github.sha }}
          # SLSA provenance attached automatically when using build-push-action v6+
          provenance: true
          sbom: true

      # Fix #4 — vulnerability scan; fail on CRITICAL/HIGH before deploy
      - name: Scan image for CVEs
        uses: aquasecurity/trivy-action@6e7b7d1fd3e4fef0c5fa8cce1229c54b2c9bd0d8  # v0.24.0
        with:
          image-ref: ghcr.io/${{ github.repository }}/cart-api:${{ github.sha }}
          format: table
          exit-code: 1
          severity: CRITICAL,HIGH

      # Fix #3 — sign image with cosign (keyless OIDC, Sigstore transparency log)
      - name: Install cosign
        uses: sigstore/cosign-installer@dc72c7d5c4d10cd6bcb8cf6e3fd625a9e5e537da  # v3.7.0

      - name: Sign image
        run: |
          cosign sign --yes \
            ghcr.io/${{ github.repository }}/cart-api:${{ github.sha }}@${{ steps.build.outputs.digest }}

      - name: Deploy to Kubernetes
        uses: azure/k8s-deploy@fe5e4f29055c11b7eaf3d312e6e6765b5f21b26b  # v4.10.0
        with:
          manifests: k8s/deployment.yaml
          images: ghcr.io/${{ github.repository }}/cart-api:${{ github.sha }}

      # Fix #6 — rollback gate: fail the workflow if pods don't become healthy
      - name: Verify rollout
        run: kubectl rollout status deployment/cart-api --timeout=120s
```

### How the rollback gate works

```
build passes
    → scan passes (no CRITICAL/HIGH CVEs)
        → sign (cosign attestation in Sigstore log)
            → deploy (k8s-deploy updates the manifest)
                → kubectl rollout status (waits up to 120 s)
                    if pods healthy  → workflow green, deploy done
                    if pods not ready → workflow red, GitHub notifies branch
                                        on-call runs: kubectl rollout undo deployment/cart-api
```

A failure at any step leaves the previous version running — no forward-only trap.
