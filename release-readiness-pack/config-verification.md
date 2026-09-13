# Configuration and environment verification

Target: `checkout-system` namespace, `checkout-api` Deployment. Static comparison completed 2026-09-13; live production values were not accessible.

| Setting | Application behavior | Kubernetes source | Verification |
| --- | --- | --- | --- |
| `PORT` | Defaults to 5000 | ConfigMap `checkout-api-config`: `5000`; container, Service and probes target 5000 | Static match |
| `LOG_LEVEL` | Defaults to `INFO` | ConfigMap: `info` | Static match; accepted by Python logging |
| `DATABASE_URL` | Required for readiness | `checkout-api-dependencies` Secret key, mandatory `secretKeyRef` | Reference configured; Secret existence/value/connectivity **unverified** |
| `REDIS_URL` | Required for readiness | Same Secret, mandatory `secretKeyRef` | Reference configured; Secret existence/value/connectivity **unverified** |

The candidate's original ConfigMap omitted both dependency settings and `/health` still returned 200 with volatile fallback labels. The Deployment now demands Secret keys, the deploy script checks their presence without printing values, and `/health` returns 503 if either is absent. This prevents a missing variable from being treated as ready. It does not test credentials or network reachability.

Before production approval, SRE must verify the Secret in the target namespace, confirm its keys are nonempty without displaying their contents, and test PostgreSQL and Redis connectivity from a staging pod using approved tooling. Confirm the endpoints, TLS policy, and least-privilege credentials with the service owners. Record the date, environment and reviewer here; do not commit secret values.
