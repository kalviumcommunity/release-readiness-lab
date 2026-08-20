# Rollback Plan - Checkout API Service

This document provides SRE runbooks for executing a rapid, safe rollback of the Checkout API deployment to the stable version in case of a production deployment failure.

## 1. Rollback Target Profile
Based on the official Release History (`docs/architecture.md`), the target stable version is **v2.3**.

- **Rollback Target Version**: `v2.3`
- **Stable Deploy Date**: `2026-06-01`
- **Known-Good Image Tag**: `kalvium/checkout-api:v2.3`

---

## 2. Emergency Rollback Procedures

Choose **one** of the two procedures below, depending on the failure mode and the deployment mechanism used.

### Method A: Kubernetes Native Rollback (Fastest)
If the deployment was upgraded in-place via an image update (e.g., via SRE pipelines), the previous replicaset is kept in Kubernetes history. Execute this command to immediately undo the rollout:

```bash
# Undo the latest deployment rollout and return to the previous revision
kubectl rollout undo deployment/checkout-api -n checkout-system
```

### Method B: Explicit Version Reversion (Declarative / GitOps)
If the deployment history was lost or if GitOps synchronization enforces state, modify and apply the deployment manifest specifying the stable `v2.3` container image tag:

```bash
# Explicitly set the deployment container image back to v2.3
kubectl set image deployment/checkout-api checkout-api=kalvium/checkout-api:v2.3 -n checkout-system
```

Alternatively, if the v2.3 manifest file `k8s/deployment.v2.3.yaml` is saved in the repository:
```bash
# Apply the known-good v2.3 manifest
kubectl apply -f k8s/deployment.v2.3.yaml
```

---

## 3. Post-Rollback Verification Checklist

Once the rollback command is executed, SREs must perform the following validation steps to confirm the service is restored to a healthy state:

### Step 1: Monitor Rollout Progress
Verify that the pods for the rollback version are rolling out successfully and the old pods are terminating:
```bash
kubectl rollout status deployment/checkout-api -n checkout-system
```
*Expected Output: `deployment "checkout-api" successfully rolled out`*

### Step 2: Check Pod Statuses
Ensure all 3 replicas are running and ready:
```bash
kubectl get pods -l app=checkout-api -n checkout-system
```
*Expected Output: All pods in `Running` status with `1/1` containers ready.*

### Step 3: Verify Version and Health Checks
Run a curl query against the internal ClusterIP service or ingress to verify the active version is restored to `v2.3` and dependencies are healthy:
```bash
# Query the health endpoint
curl http://checkout-api-service.checkout-system.svc.cluster.local/health
```
*Expected Output:*
```json
{
    "status": "healthy",
    "version": "v2.3",
    "checks": {
        "database": "connected",
        "redis": "connected"
    }
}
```

Verify the root response matches:
```bash
curl http://checkout-api-service.checkout-system.svc.cluster.local/
```
*Expected Output: `"version": "v2.3"`*

### Step 4: Examine Server Logs
Check logs for exceptions or DB connection issues:
```bash
kubectl logs -l app=checkout-api -n checkout-system --tail=50
```
*Expected Output: No python Tracebacks, database or Redis connection warnings.*
