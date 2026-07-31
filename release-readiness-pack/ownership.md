# Deployment Ownership

## Ownership Model

| Role | Owner | Responsibilities |
|------|-------|-----------------|
| Release Owner | Dev Team Lead | Approves candidate, confirms release notes, signs readiness gate |
| SRE / Operational Lead | Platform Engineering | Validates rollout execution, monitors health, manages incident escalation |
| On-Call Support | Production Support | Takes first response during the deployment window |
| Escalation Path | On-call -> SRE Lead -> Release Owner | Coordinates triage and rollback authority |

## Required Governance Sign-Off

- Release Owner sign-off required before production deployment.
- SRE sign-off required for production configuration verification.
- Rollback authority must be named before the deployment window starts.

## Current Gap

The repository currently lacks a named production owner and a recorded sign-off artifact, so ownership is unverified.
