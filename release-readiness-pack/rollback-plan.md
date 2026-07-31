# Rollback Plan

## Stable Rollback Target

The stable production baseline listed in `docs/architecture.md` is:

- `v2.3` — `Deployed (Prod - STABLE)`

This should be used as the immediate rollback target for any failed `v2.4` rollout.

## Rollback Steps

1. Pause or halt the rollout and mitigate traffic exposure.
2. Revert the deployment image reference from `kalvium/checkout-api:v2.4` to `kalvium/checkout-api:v2.3`.
3. Apply the prior stable Kubernetes Deployment revision.
4. Confirm the service is serving traffic again through the stable pods.

Pseudo-commands:

```bash
kubectl -n checkout-system set image deployment/checkout-api checkout-api=kalvium/checkout-api:v2.3
kubectl -n checkout-system rollout undo deployment/checkout-api
kubectl -n checkout-system rollout status deployment/checkout-api
kubectl -n checkout-system get pods -n checkout-system
kubectl -n checkout-system get svc checkout-api-service
```

## Verification After Rollback

Post-rollback verification should include:

- `/health` returns `200`
- service endpoints remain available through the ClusterIP service
- the stable version is confirmed as `v2.3` in the application response
- the rollback target is stable for the next release window

## Known Risk in the Current Candidate

The rollback plan is documented but not operationally tested against the target cluster; therefore the rollback procedure remains a documented control, not a verified production rehearsal.
