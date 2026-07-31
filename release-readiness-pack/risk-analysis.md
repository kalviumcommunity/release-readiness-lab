# Risk Analysis

## Risk Matrix

| Risk | Severity | Likelihood | Mitigation | Owner |
|------|----------|------------|------------|-------|
| Missing `DATABASE_URL` / `REDIS_URL` in target manifest | High | High | Inject required service connection values via Kubernetes Secret or managed config; validate connectivity before rollout | SRE / Platform Engineering |
| Container image build not verified in the target environment | High | Medium | Re-run build in CI with BuildKit and scan the resulting image | Release Owner |
| No verified rollback rehearsal against the target cluster | High | Medium | Perform a recorded rollback drill before cutover and document the exact commands | SRE / Operational Lead |
| Single-replica or single-tenant dependency risk in deployment topology | Medium | Medium | Confirm HPA / anti-affinity / node distribution; verify replica behavior | Platform Engineering |
| No named production sign-off or ownership record | Medium | High | Capture sign-off checklist and deployment owner in the release pack | Release Owner |
| Unpinned or unvetted dependency drift | Medium | Low | Keep exact pins, scan periodically, and update with policy | Security / Dev Team |

## Worst Open Risk

The highest-confidence production blocker is the absence of the required PostgreSQL and Redis runtime configuration in the deployed Kubernetes config. This makes the service fall back to non-production-safe in-memory behavior and therefore prevents a reliable production readiness call.
