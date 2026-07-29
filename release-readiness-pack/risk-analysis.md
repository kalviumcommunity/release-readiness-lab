# Risk Analysis

| Risk | Severity | Likelihood | Mitigation | Owner |
|---|---|---|---|---|
| Missing `DATABASE_URL` and `REDIS_URL` in production config causes volatile fallback behavior | High | High | Inject both values from secrets or external secret management and fail readiness if they are absent | SRE Lead + Application Owner |
| `/health` reports healthy even when it is using fallback dependencies | High | High | Change health semantics so degraded dependency paths fail readiness or report degraded status | Application Owner |
| No formal operational approver or named deploy owner is present in the repository | High | Medium | Assign a release owner, SRE lead, and on-call engineer before deploy approval | Release Manager |
| Container validation was not reproducible in this workstation because Docker was unavailable | Medium | High | Re-run the image build and smoke test in CI or on a Docker-enabled runner before shipping | Platform Engineer |
| Rollback depends on preserving and restoring the known-good `v2.3` image and matching config | Medium | Medium | Archive the stable release bundle and test the rollback path in advance | SRE Lead |
| Supply-chain control is limited because there is no lockfile or hash-locked constraint set | Medium | Medium | Add hash-locked dependency constraints or a generated lock artifact | Application Owner |

## Worst Open Risk

The worst open risk is the missing production dependency configuration, because it directly changes runtime behavior while still presenting the service as healthy.
