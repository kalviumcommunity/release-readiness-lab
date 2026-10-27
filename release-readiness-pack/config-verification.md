# Configuration verification

Compared `app/app.py`, `k8s/configmap.yaml`, `k8s/deployment.yaml`, and `docs/architecture.md` on 2026-10-27.

| Variable | Source | Expected/observed | Status |
|---|---|---|---|
| `PORT` | ConfigMap | `5000`; app fallback is `5000` | Verified |
| `LOG_LEVEL` | ConfigMap | `info`; app fallback is `INFO` | Verified |
| `DATABASE_URL` | Secret required by architecture | Missing from ConfigMap and Deployment | **BLOCKER** |
| `REDIS_URL` | Secret required by architecture | Missing from ConfigMap and Deployment | **BLOCKER** |

The application currently returns HTTP 200 and `status: healthy` when either URL is absent, while reporting `warning_fallback_sqlite` and `warning_fallback_local`. Those fallbacks are volatile and do not meet the documented PostgreSQL/Redis production architecture. URLs must be supplied through a platform-managed Kubernetes Secret (not committed), referenced with `envFrom.secretRef` or explicit `secretKeyRef`, and verified in a staging deployment without printing values.

## Required before Go

1. Create `checkout-api-secrets` in `checkout-system` using the production secret manager.
2. Reference it from the Deployment for `DATABASE_URL` and `REDIS_URL`.
3. Make `/health` fail readiness when required dependencies are unavailable, or obtain an explicit SRE-approved exception for the fallback behavior.
4. Run a staging smoke test with redacted logs and record the result.
