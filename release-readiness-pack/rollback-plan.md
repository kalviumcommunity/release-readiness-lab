# Rollback Plan

## Stable Target

The documented stable production version is `v2.3` in `docs/architecture.md`.

## Primary Rollback Approach

If the `v2.4` deployment causes an incident, roll back to the last known-good deployment revision or explicitly reset the image to `kalvium/checkout-api:v2.3`.

### Option A: Deployment revision rollback

```bash
kubectl -n checkout-system rollout history deployment/checkout-api
kubectl -n checkout-system rollout undo deployment/checkout-api
kubectl -n checkout-system rollout status deployment/checkout-api --timeout=120s
```

### Option B: Explicit image rollback

```bash
kubectl -n checkout-system set image deployment/checkout-api \
	checkout-api=kalvium/checkout-api:v2.3
kubectl -n checkout-system rollout status deployment/checkout-api --timeout=120s
```

## Verification After Rollback

1. Confirm all pods are ready:

```bash
kubectl -n checkout-system get pods
```

2. Confirm the service responds on the stable version:

```bash
kubectl -n checkout-system port-forward svc/checkout-api-service 8080:80
curl -s http://127.0.0.1:8080/
curl -s http://127.0.0.1:8080/health
```

3. Confirm the health response is not degraded and that dependency configuration is intact.

## Rollback Preconditions

- Preserve the `v2.3` image in the registry before promoting `v2.4`.
- Keep the last known-good configuration bundle available so configuration and code can be rolled back together if needed.
- Record the rollback event in the incident log and notify the release owner, SRE lead, and on-call engineer.

## Notes

This plan is operationally valid, but the current repository does not yet provide the production secrets/configuration needed to make the service healthy after rollback if the same missing-environment problem is still present. That configuration gap must be closed before a production go decision.
