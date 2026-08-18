# Rollback Plan

This document outlines the procedure to immediately revert the checkout-api deployment from the v2.4 release candidate to the last known-good stable release (**v2.3**), in the event of post-deployment service disruption.

## 1. Rollback Targets & Trigger Criteria

- **Target Stable Version**: `v2.3`
- **Trigger Conditions**:
  - **High Error Rate**: HTTP 5xx error rate > 1% on the `/` or `/health` endpoints.
  - **Dependency Failures**: Local database or redis fallbacks are triggered due to connection loss.
  - **Liveness/Readiness Failures**: Pods crash-looping or failing Kubernetes probes.

---

## 2. Step-by-Step Rollback Execution

If any trigger condition is met during or immediately after the deployment window, the SRE / Release Operator must run the following steps:

### Step 1: Revert Deployment Manifest (Option A - Git Revert & Re-apply)
Checkout the production-stable tag/manifest and re-apply:
```bash
# Revert to stable deployment manifest or edit image version to v2.3
kubectl set image deployment/checkout-api checkout-api=kalvium/checkout-api:v2.3 -n checkout-system
```

### Step 2: Kubernetes Native Rollback (Option B - Native Rollback)
If the deployment history was preserved and not corrupted, perform a native rollout undo:
```bash
# Check rollout history
kubectl rollout history deployment/checkout-api -n checkout-system

# Undo rollout to revert to the previous revision (v2.3)
kubectl rollout undo deployment/checkout-api -n checkout-system
```

### Step 3: Monitor Rollout Progress
```bash
# Verify the status of the rollout
kubectl rollout status deployment/checkout-api -n checkout-system
```

---

## 3. Post-Rollback Verification Checklist

Once the rollback is completed, execute the following commands to verify service restoration:

1. **Verify Pod Status**:
   ```bash
   kubectl get pods -n checkout-system -l app=checkout-api
   ```
   *Expected outcome: All pods show `Running` status with `Ready: 1/1`.*

2. **Test API Health**:
   ```bash
   # Extract service IP or use port-forwarding
   kubectl port-forward svc/checkout-api-service 5000:80 -n checkout-system
   
   # Curl root and health check endpoints
   curl http://localhost:5000/
   curl http://localhost:5000/health
   ```
   *Expected outcome:*
   - Root response: `{"service": "checkout-api", "version": "v2.3", "message": "..."}`
   - Health response: status code `200` with `status: healthy` and database & redis status showing `connected` (no sqlite or local memory fallbacks).
