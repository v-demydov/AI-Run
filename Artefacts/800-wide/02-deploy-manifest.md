---
kata: 8.W.2
date: 2026-07-30
service: cart-api
---

# Kubernetes Manifest — cart-api

## Step 1 — Generated manifest (first draft)

```yaml
# cart-api Deployment + Service
apiVersion: apps/v1
kind: Deployment
metadata:
  name: cart-api
  labels:
    app: cart-api
spec:
  replicas: 3
  selector:
    matchLabels:
      app: cart-api
  template:
    metadata:
      labels:
        app: cart-api
    spec:
      containers:
        - name: cart-api
          image: registry.example.com/cart-api:latest
          ports:
            - containerPort: 8080
          env:
            - name: DATABASE_URL
              value: "postgres://user:password@postgres-host:5432/cartdb"
            - name: DIAL_API_KEY
              value: "sk-live-abc123secret"
          resources:
            requests:
              memory: "256Mi"
              cpu: "100m"
---
apiVersion: v1
kind: Service
metadata:
  name: cart-api
spec:
  selector:
    app: cart-api
  ports:
    - protocol: TCP
      port: 80
      targetPort: 8080
  type: ClusterIP
```

---

## Step 2 — Fresh-session adversarial audit

> Audited in isolation — no access to the generation context.

### Audit table

| # | Missing control | Why it matters | One-line fix |
|---|-----------------|----------------|-------------|
| 1 | `resources.limits` absent | Without limits a misbehaving pod can consume all node memory/CPU, evicting neighbours; scheduler cannot bin-pack reliably | Add `limits: {memory: "512Mi", cpu: "500m"}` under `resources:` |
| 2 | `readinessProbe` absent | Kubernetes sends traffic to a pod the moment the container starts — before the app is ready to serve. Rolling deploy silently routes live requests to a booting pod | Add `readinessProbe: {httpGet: {path: /healthz, port: 8080}, initialDelaySeconds: 5, periodSeconds: 10}` |
| 3 | `livenessProbe` absent | A deadlocked pod stays in service indefinitely; no automatic restart | Add `livenessProbe: {httpGet: {path: /healthz, port: 8080}, initialDelaySeconds: 15, periodSeconds: 20, failureThreshold: 3}` |
| 4 | Secrets as plaintext `env.value` | `DATABASE_URL` and `DIAL_API_KEY` are visible in `kubectl get pod -o yaml`, stored in etcd unencrypted, and leak into CI logs | Replace with `env.valueFrom.secretKeyRef`; create a `Secret` object (managed by Vault or Sealed Secrets) |
| 5 | No `strategy: RollingUpdate` with `maxUnavailable: 0` | Default `maxUnavailable: 25%` means 1 of 3 replicas is taken down before the new one is ready — the service runs on 2 pods during deploy, and if the new pod fails readiness the deploy stalls with reduced capacity | Add `strategy: {type: RollingUpdate, rollingUpdate: {maxUnavailable: 0, maxSurge: 1}}` |
| 6 | `image: :latest` tag | Latest is re-pulled on every restart, bypasses the image cache, and makes rollback (`kubectl rollout undo`) non-deterministic — you don't know which image version you're reverting to | Pin to an immutable digest or semver tag: `cart-api:1.4.2` or `cart-api@sha256:…` |
| 7 | No `minReadySeconds` | A pod that passes its readiness probe for 1 second then crashes still counts as "available"; traffic hits it before it proves stable | Add `minReadySeconds: 10` at the Deployment spec level |
| 8 | No `PodDisruptionBudget` | `kubectl drain` (node maintenance, cluster upgrade) can evict all 3 pods simultaneously, causing a full outage | Create a `PodDisruptionBudget` with `minAvailable: 2` |

### Verdict

8 gaps on a first draft. The two that cause customer-visible outages in a rolling deploy are **#2 (readinessProbe)** and **#5 (maxUnavailable: 0)**. The one that causes a security incident is **#4 (plaintext secrets)**. None of these would be caught by a syntax linter or `kubectl apply --dry-run`.

---

## Step 3 — Fixed manifest

```yaml
# cart-api — production-ready
apiVersion: v1
kind: Secret
metadata:
  name: cart-api-secrets
type: Opaque
# Values base64-encoded; manage with Vault / Sealed Secrets in production
data:
  DATABASE_URL: <base64-encoded-value>
  DIAL_API_KEY: <base64-encoded-value>
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: cart-api
  labels:
    app: cart-api
spec:
  replicas: 3
  minReadySeconds: 10                           # fix #7
  strategy:                                     # fix #5
    type: RollingUpdate
    rollingUpdate:
      maxUnavailable: 0
      maxSurge: 1
  selector:
    matchLabels:
      app: cart-api
  template:
    metadata:
      labels:
        app: cart-api
    spec:
      containers:
        - name: cart-api
          image: registry.example.com/cart-api:1.4.2   # fix #6 — pinned tag
          ports:
            - containerPort: 8080
          env:
            - name: DATABASE_URL                        # fix #4 — from Secret
              valueFrom:
                secretKeyRef:
                  name: cart-api-secrets
                  key: DATABASE_URL
            - name: DIAL_API_KEY
              valueFrom:
                secretKeyRef:
                  name: cart-api-secrets
                  key: DIAL_API_KEY
          resources:                                    # fix #1 — limits added
            requests:
              memory: "256Mi"
              cpu: "100m"
            limits:
              memory: "512Mi"
              cpu: "500m"
          readinessProbe:                               # fix #2 — traffic gate
            httpGet:
              path: /healthz
              port: 8080
            initialDelaySeconds: 5
            periodSeconds: 10
            failureThreshold: 3
          livenessProbe:                                # fix #3 — deadlock restart
            httpGet:
              path: /healthz
              port: 8080
            initialDelaySeconds: 15
            periodSeconds: 20
            failureThreshold: 3
---
apiVersion: v1
kind: Service
metadata:
  name: cart-api
spec:
  selector:
    app: cart-api
  ports:
    - protocol: TCP
      port: 80
      targetPort: 8080
  type: ClusterIP
---
apiVersion: policy/v1
kind: PodDisruptionBudget                       # fix #8 — drain protection
metadata:
  name: cart-api-pdb
spec:
  minAvailable: 2
  selector:
    matchLabels:
      app: cart-api
```

### Rollback path

```bash
# See rollout history (works because image tag is now pinned)
kubectl rollout history deployment/cart-api

# Roll back one revision
kubectl rollout undo deployment/cart-api

# Roll back to a specific revision
kubectl rollout undo deployment/cart-api --to-revision=3
```
