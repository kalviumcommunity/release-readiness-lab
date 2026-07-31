# Configuration Verification

## Target Configuration Sources

The application reads the following environment variables from the runtime environment:

- `PORT` with default `5000`
- `LOG_LEVEL` with default `INFO`
- `DATABASE_URL` required for PostgreSQL connectivity
- `REDIS_URL` required for Redis connectivity

These values are defined by the application code in `app/app.py` and are also referenced in `docs/architecture.md`.

## Verified Manifest Findings

The Kubernetes ConfigMap in `k8s/configmap.yaml` currently contains:

- `LOG_LEVEL: "info"`
- `PORT: "5000"`

The manifest does not include the required production service connection variables:

- `DATABASE_URL`
- `REDIS_URL`

## Production Impact

The application intentionally falls back to non-production-safe defaults when these vars are absent:

- `DATABASE_URL` absent => warning fallback to unstable SQLite only
- `REDIS_URL` absent => warning fallback to local in-memory cache only

That fallback behavior is explicitly documented in `app/app.py` and is unacceptable for a production deployment without a verified replacement.

## Verification Status

- `PORT` and `LOG_LEVEL`: present in config manifest
- `DATABASE_URL`: missing from the target release manifest
- `REDIS_URL`: missing from the target release manifest

## Required Production Correction

Before any `go` decision, the deployment must verify that these settings are injected from a managed secret/config layer and that the actual service endpoints are reachable from the cluster.
