# Configuration Verification Checklist

This document details the configuration parameters audited for the Checkout API v2.4 deployment and verifies them against the target production environments.

## 1. Audited Configuration Variables

The application processes configuration parameters from the system environment at startup. Below is the mapping of defined variables, their source, and production statuses:

| Environment Variable | Source | Expected Value (Prod) | Default / Fallback Behavior | SRE Status |
|---|---|---|---|---|
| `PORT` | `ConfigMap` | `5000` | Defaults to `5000` if not set | Verified |
| `LOG_LEVEL` | `ConfigMap` | `info` | Defaults to `"INFO"` if not set | Verified |
| `DATABASE_URL` | `Secret` | `postgresql://...` | Fallback to unstable, volatile in-memory SQLite | **CRITICAL FIX APPLIED** (Moved to Secret) |
| `REDIS_URL` | `Secret` | `redis://...` | Fallback to volatile local in-memory dict cache | **CRITICAL FIX APPLIED** (Moved to Secret) |

## 2. Identified Risks & Gaps in Original Manifests

During SRE audit, the following configuration gaps were identified:
- **Sensitive Connection Strings**: `DATABASE_URL` and `REDIS_URL` were completely omitted from [configmap.yaml](file:///d:/Kalvium/release-readiness-lab/k8s/configmap.yaml).
- **Volatile Fallback Fallouts**: If deployed as-is, the application would default to in-memory SQLite and a local Python dictionary for caching. This means state (carts, checkout sessions) would be lost on Pod restart/scale operations, causing data corruption and severe user degradation.
- **Exposure Risk**: Even if added to the ConfigMap, it would expose database credentials in plain text.

## 3. Remediation Details

To align with SRE security and reliability standards, we implemented the following changes:
1. **Secrets Deployment**: Created [secret.yaml](file:///d:/Kalvium/release-readiness-lab/k8s/secret.yaml) to store `DATABASE_URL` and `REDIS_URL` as Kubernetes Opaque Secrets.
2. **Secrets Mapping**: Modified the `envFrom` section in [deployment.yaml](file:///d:/Kalvium/release-readiness-lab/k8s/deployment.yaml) to map `checkout-api-secrets` keys as container environment variables.
3. **Deployment script update**: Integrated the Secret into the deployment flow in [deploy.sh](file:///d:/Kalvium/release-readiness-lab/scripts/deploy.sh).
