# Rollback plan

**Known-good target:** `v2.3`, documented as **Prod - STABLE** in `docs/architecture.md`. The candidate is `v2.4`.

## Steps

```bash
kubectl -n checkout-system rollout history deployment/checkout-api
kubectl -n checkout-system set image deployment/checkout-api \
  checkout-api=kalvium/checkout-api:v2.3
kubectl -n checkout-system rollout status deployment/checkout-api --timeout=180s
kubectl -n checkout-system get pods -l app=checkout-api
kubectl -n checkout-system get deployment checkout-api \
  -o jsonpath='{.spec.template.spec.containers[0].image}{"\n"}'
```

If the previous ReplicaSet is available and image rollback is insufficient:

```bash
kubectl -n checkout-system rollout undo deployment/checkout-api
kubectl -n checkout-system rollout status deployment/checkout-api --timeout=180s
```

Verify the Service, readiness probes, `/health`, and a representative checkout smoke test. Confirm error rate/latency return to baseline, then announce rollback completion. Do not roll back database migrations without the database owner’s approved reverse-migration plan.

## Test status

Commands are reviewed but not executed against a cluster: no Kubernetes API was available on 2026-10-27. A staging rollback rehearsal and captured output are mandatory before production Go.
