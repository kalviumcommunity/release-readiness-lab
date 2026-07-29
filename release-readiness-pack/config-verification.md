# Configuration Verification Checklist

## Scope

Reviewed `app/app.py`, `k8s/configmap.yaml`, and `k8s/deployment.yaml` against the expected production settings in `docs/architecture.md`.

## Checklist

| Item | Expected for production | Current state | Evidence | Status |
|---|---|---|---|---|
| `PORT` | Set to the service port used by the container | Set to `5000` in the ConfigMap | `k8s/configmap.yaml` | Pass |
| `LOG_LEVEL` | Explicit log level | Set to `info` | `k8s/configmap.yaml` | Pass |
| `DATABASE_URL` | Present and backed by a production database secret | Missing from ConfigMap; app falls back to in-memory SQLite behavior | `app/app.py`, `k8s/configmap.yaml` | Fail |
| `REDIS_URL` | Present and backed by a production cache secret | Missing from ConfigMap; app falls back to local in-memory cache behavior | `app/app.py`, `k8s/configmap.yaml` | Fail |
| Health status semantics | Degraded dependencies should not report healthy | `/health` returns `status: healthy` even when fallback paths are active | Runtime validation | Fail |
| Deployment environment source | Config should come from secrets-backed production inputs | Deployment only uses `envFrom` the ConfigMap | `k8s/deployment.yaml` | Fail |
| Runtime version | Python 3.11 per architecture doc | Dockerfile uses `python:3.11-slim` | `docs/architecture.md`, `app/Dockerfile` | Pass |
| Pod replica count | At least 3 for basic availability | `replicas: 3` | `k8s/deployment.yaml` | Pass |
| Probe coverage | Readiness and liveness probes present | Both probes point to `/health` | `k8s/deployment.yaml` | Pass, but probe semantics are weak |

## Findings

- The configuration is incomplete for production because the application depends on `DATABASE_URL` and `REDIS_URL`, but the ConfigMap only supplies `PORT` and `LOG_LEVEL`.
- The current application logic treats missing dependencies as warnings instead of failures, so the Kubernetes probes can report healthy while the service is operating in a non-production fallback mode.
- Production readiness requires secret-backed dependency configuration and a health model that distinguishes healthy from degraded.

## Required Before Go

1. Provide real `DATABASE_URL` and `REDIS_URL` values through production secrets or external secret management.
2. Confirm the service fails readiness when the required backing services are absent.
3. Re-run runtime validation with production-like environment variables present.
