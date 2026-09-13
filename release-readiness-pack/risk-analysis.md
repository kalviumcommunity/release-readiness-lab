# Operational risk register

Assessment date: 2026-09-13. **Open High risks block release**; passing unit tests cannot offset them. Role owners below identify the accountable function, but named people must accept the roles in `ownership.md`.

| ID | Risk / evidence | Severity | Likelihood | Mitigation and exit evidence | Owner | State |
| --- | --- | --- | --- | --- | --- | --- |
| R1 | Target Secret values and PostgreSQL/Redis connectivity unverified; original candidate omitted both | High | High | Verify approved Secret, live connectivity and TLS from staging; attach redacted results | SRE Lead | Open |
| R2 | Rollback to documented stable v2.3 has not been rehearsed; registry digest unconfirmed | High | Medium | Verify digest and rehearse rollback; record recovery time and v2.3 health | Release Owner / SRE | Open |
| R3 | No named on-call, escalation contact or signed production approval | High | High | Assign people and window; obtain recorded sign-off | Release Owner | Open |
| R4 | PR CI Docker dry-run build passes, but no immutable published v2.4 image or staged rollout evidence | High | Medium | Record published image digest, staged rollout and smoke test | Dev Lead | Open |
| R5 | `/health` tests only config presence, not actual DB/Redis reachability | High | Medium | Add live dependency checks or separate preflight/monitoring; prove failover behavior | Dev Lead / SRE | Open |
| R6 | Container image and base image use mutable tags; transitive dependencies not fully locked | Medium | Medium | Pin digests, create lock/SBOM, scan built image | Dev Lead | Open |
| R7 | No evidence of image user privileges or container security scan | Medium | Medium | Run image scan; review non-root, filesystem and runtime policy | Security / Dev Lead | Open |
| R8 | Three replicas share one Kubernetes deployment and unspecified backing service resilience | Medium | Medium | Validate DB/Redis HA and failure-domain placement; test disruption response | SRE Lead | Open |

The earlier `pip-audit` findings for Flask and pytest were mitigated by pin upgrades and a repeat scan with no known findings. This does not close the separate runtime and image risks.
