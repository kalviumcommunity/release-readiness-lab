# Configuration Verification Checklist

This document details the configuration audit performed on the Checkout API v2.4 manifests and application logic.

## 1. Environment Variable Inventory & Targets

| Variable Name | Source Location | Description | Default/Fallback | Operational Status in Manifests |
|---|---|---|---|---|
| `PORT` | `app/app.py:60` | Server listening port | `5000` (Local) | Configured in ConfigMap (`PORT: "5000"`) |
| `LOG_LEVEL` | `app/app.py:9` | Logging severity | `INFO` | Configured in ConfigMap (`LOG_LEVEL: "info"`) |
| `DATABASE_URL`| `app/app.py:27` | Connection URI to PostgreSQL | None (trig. SQLite fallback) | **OMITTED** in original ConfigMap. Added in updated ConfigMap. |
| `REDIS_URL` | `app/app.py:28` | Connection URI to Redis Cache | None (trig. local cache fallback) | **OMITTED** in original ConfigMap. Added in updated ConfigMap. |

---

## 2. Configuration Gaps Identified

### Gap A: Missing Database & Redis Configurations
The original developer-provided `k8s/configmap.yaml` did not define `DATABASE_URL` or `REDIS_URL`. This causes the application to fall back to:
- **In-Memory SQLite Database** (`warning_fallback_sqlite`): An ephemeral database created in the container's RAM.
- **Local Dictionary Cache** (`warning_fallback_local`): An in-memory cache local to each Gunicorn worker process.

#### Production Risk: Ephemeral & Split-Brain State
1. **No Shared State**: Since the deployment defines `replicas: 3`, there are three independent pods. If a client writes cart details to Pod 1, Pod 2 and Pod 3 will not see those cart details. Transactions, cart processing, and discounts will fail due to data inconsistency.
2. **Ephemeral Lifespan**: Containers are volatile. If a pod crashes or restarts, all data written to the in-memory SQLite database is instantly deleted.

---

## 3. Health Check Logic Gap (Mock Connectivity)

We audited the `/health` endpoint logic in `app/app.py#L25-L57`:
```python
    if db_url:
        db_status = "connected"
        logger.info("Database status: CONNECTED")
    else:
        db_status = "warning_fallback_sqlite"
        ...
```
### SRE Finding: Non-functional Probe
- The application **does not establish network connectivity** to the database or Redis server to verify health. It merely tests if the `DATABASE_URL` and `REDIS_URL` strings are defined in the environment.
- If the PostgreSQL instance is completely down, but `DATABASE_URL` is set, the health probe will return `200 OK` and status `"connected"`.
- Kubernetes will keep routing client traffic to pods that are in reality completely broken, resulting in SRE detection blindspots and client-facing HTTP 500 errors.

---

## 4. Production Secret Management Recommendation

In our updated `k8s/configmap.yaml`, we added placeholders for `DATABASE_URL` and `REDIS_URL`. However, storing database credentials in plain-text inside ConfigMaps is a **critical security risk**.

### Remediation Plan
1. Define a Kubernetes Secret containing base64-encoded credentials:
   ```yaml
   apiVersion: v1
   kind: Secret
   metadata:
     name: checkout-api-secrets
     namespace: checkout-system
   type: Opaque
   data:
     DATABASE_URL: cG9zdGdyZXNxbDovL2NoZWNrb3V0X3VzZXI6Y2hlY2tvdXRfc2VjdXJlX3Bhc3N3b3JkQGNoZWNrb3V0LWRiLmNoZWNrb3V0LXN5c3RlbS5zdmMuY2x1c3Rlci5sb2NhbDo1NDMyL2NoZWNrb3V0X2Ri
     REDIS_URL: cmVkaXM6Ly9jaGVja291dC1yZWRpcy5jaGVja291dC1zeXN0ZW0uc3ZjLmNsdXN0ZXIubG9jYWw6NjM3OS8w
   ```
2. Reference the secret in `k8s/deployment.yaml`:
   ```yaml
         env:
         - name: DATABASE_URL
           valueFrom:
             secretKeyRef:
               name: checkout-api-secrets
               key: DATABASE_URL
         - name: REDIS_URL
           valueFrom:
             secretKeyRef:
               name: checkout-api-secrets
               key: REDIS_URL
   ```
This ensures sensitive credentials are encrypted at rest and not exposed in version control.
