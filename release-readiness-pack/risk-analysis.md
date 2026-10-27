# Risk analysis

| Risk | Severity | Likelihood | Mitigation | Owner |
|---|---|---|---|---|
| Production DB/cache URLs absent; volatile fallbacks can lose state | High | High | Inject managed Secret values, fail readiness, run staging smoke test | Application Owner |
| Known vulnerabilities in original dependency pins | High | Medium | Updated pins; rerun pip-audit in CI and publish an SBOM | Application Owner |
| Rollback has not been rehearsed on a cluster | High | Medium | Rehearse v2.4 → v2.3 and capture rollout/health evidence | SRE Lead |
| Container build and Kubernetes validation unavailable locally | Medium | Medium | Require CI image build and staging deployment gate | Release Owner |
| Image tag is mutable and not digest-pinned | Medium | Medium | Promote an immutable digest and record it in the release ticket | SRE Lead |
| Health endpoint reports healthy despite dependency warnings | High | High | Make readiness dependency-aware or approve a documented exception | Application Owner |
| No named deploy-window on-call or approval record | Medium | Medium | Complete ownership matrix and obtain release/sign-off approval | Release Owner |
| Three replicas share one deployment and no disruption policy is defined | Low | Medium | Add PDB/availability policy and verify capacity before rollout | SRE Lead |

The two High/High risks are open release blockers.
