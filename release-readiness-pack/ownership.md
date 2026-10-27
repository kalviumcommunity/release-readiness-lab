# Deployment ownership

Names and contact handles must be completed in the release ticket before approval; roles must not remain anonymous.

| Role | Accountability | Required contact |
|---|---|---|
| Release Owner | Coordinates gate, change record, approval, and go/no-go | Release Engineering / named assignee |
| Application Owner | Fixes config/health behavior and validates checkout | Checkout team / named assignee |
| SRE / Operational Lead | Executes deployment, observes metrics, and owns rollback | SRE / named assignee |
| Deploy-window On-Call | First responder during the agreed window | On-call rotation / page target |
| Escalation | Incident Commander plus database/cache owners for dependency incidents | Incident rotation / page target |

## Handoff checklist

- [ ] Deploy window, timezone, and change ticket recorded.
- [ ] Release Owner, Application Owner, SRE Lead, and on-call names/pages recorded.
- [ ] Rollback approver and v2.3 image availability confirmed.
- [ ] Monitoring dashboard, alert route, and incident channel linked.
- [ ] Approval/sign-off captured after all High risks are closed.
