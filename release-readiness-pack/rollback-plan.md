# Rollback runbook — v2.4 to v2.3

`docs/architecture.md` identifies **v2.3** as the current stable production release. This is a documented target, not verification that the registry tag or cluster revision exists. Rollback is **written but not tested**; it is a release blocker until rehearsed in staging.

## Before deployment

Release Owner records the current image digest, rollout revision, v2.3 image digest, dashboard baseline and any schema/data changes. SRE confirms that `kalvium/checkout-api:v2.3` resolves to the approved known-good digest and remains pullable. Verify that v2.4 introduces no irreversible schema or data change; otherwise obtain a separate data rollback plan. Keep the v2.3 manifest and config snapshot in a secured change record. Do not deploy if any prerequisite fails.

```sh
kubectl -n checkout-system get deployment checkout-api -o jsonpath='{.spec.template.spec.containers[0].image}'
kubectl -n checkout-system rollout history deployment/checkout-api
kubectl -n checkout-system get pods -l app=checkout-api
```

## Trigger and execution

The on-call SRE initiates rollback for failed rollout, sustained 5xx/latency regression, failed dependency checks, or data-integrity alarms. Stop traffic expansion first. If the previous rollout revision is confirmed as v2.3, use `kubectl rollout undo deployment/checkout-api --to-revision=<recorded-v2.3-revision> -n checkout-system`. Otherwise restore the approved v2.3 digest explicitly:

```sh
kubectl -n checkout-system set image deployment/checkout-api checkout-api=kalvium/checkout-api@sha256:<approved-v2.3-digest>
kubectl -n checkout-system rollout status deployment/checkout-api --timeout=180s
kubectl -n checkout-system get deployment checkout-api -o jsonpath='{.spec.template.spec.containers[0].image}'
kubectl -n checkout-system get pods -l app=checkout-api
```

The digest placeholder must be replaced from the verified registry record **before** deployment. Do not paste a guessed digest. If rollout stalls, page the Incident Commander and retain the failing pod events/logs; do not repeatedly toggle versions.

## Verify and close

Confirm three available replicas, v2.3 image digest, successful `/health` from the Service, real checkout smoke transaction, dependency connectivity, and normal 5xx/latency/error-budget metrics for at least 15 minutes. SRE records command output, timestamps and incident link. Release Owner informs stakeholders, freezes v2.4, and opens a root-cause follow-up. The staging rehearsal and timed recovery result are still pending.
