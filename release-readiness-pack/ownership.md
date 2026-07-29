# Ownership

## Release Roles

| Role | Responsibility | Assigned Owner |
|---|---|---|
| Release Owner | Owns the go/no-go decision, change record, and release timing | Release Engineering |
| Operational Lead | Confirms production configuration, probes, and rollback readiness | Site Reliability Engineering |
| Application Owner | Confirms app behavior, dependency expectations, and runtime changes | Checkout API Team |
| On-Call Support | Handles first-line incident response during the deployment window | Checkout API on-call rotation |
| Escalation Path | Escalates unresolved issues to management and platform support | SRE Manager -> Platform Manager -> Engineering Manager |

## Deployment Window Controls

- Freeze unrelated changes during the release window.
- Require the release owner and operational lead to sign off before production deployment.
- Keep on-call coverage active for the full rollback window.
- Record the exact deployment timestamp, revision, and approver names in the change ticket.

## Approval Requirement

This repository is not approvable until the release owner, operational lead, and on-call support are explicitly named in the change record for the deployment window.
