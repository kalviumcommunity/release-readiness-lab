# Rollback Plan (Tested Steps)

Goal: provide a fast, tested rollback path to return the production system to a known-good state with minimal downtime.

Known-good version
- Known-good image tag: `kalvium/checkout-api:v2.3` (replace with the last production tag)

Rollback methods

1) Kubernetes native - `kubectl rollout undo` (when using Deployments):

```bash
kubectl -n checkout-system rollout undo deployment/checkout-api
kubectl -n checkout-system rollout status deployment/checkout-api --timeout=120s
kubectl -n checkout-system get pods -l app=checkout-api -o wide
```

2) Explicit image re-point:

```bash
kubectl -n checkout-system set image deployment/checkout-api checkout-api=kalvium/checkout-api:v2.3
kubectl -n checkout-system rollout status deployment/checkout-api --timeout=120s
```

3) Helm rollback (if using Helm):

```bash
helm -n checkout-system history checkout-api
helm -n checkout-system rollback checkout-api <REVISION>
```

Testing the rollback plan
- Execute these steps in a staging cluster and capture output to `release-readiness-pack/evidence/rollback-test-<date>.txt`.
- Status: NOT TESTED in staging yet.

Post-rollback verification
- Run `/health` and critical smoke tests.
- Monitor logs and SLOs for 15 minutes.
