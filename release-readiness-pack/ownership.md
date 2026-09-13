# Deployment ownership and sign-off

The repository has no verified production roster. The following roles are required; no named person or approval is invented for this assignment.

| Role | Responsibility | Named assignee / acceptance |
| --- | --- | --- |
| Release Owner | Schedule, gate review, coordinate deploy and decision record | **Unassigned** |
| SRE / Operational Lead | Verify target environment, execute deployment and rollback rehearsal | **Unassigned** |
| On-call Support | Watch metrics for the deploy window and first 24 hours; act on triggers | **Unassigned** |
| Dev Lead | Confirm image, tests, schema/data compatibility and fix defects | **Unassigned** |
| Incident Commander / escalation | Coordinate incident if rollback fails or customer impact occurs | **Unassigned** |

Before a go decision, fill in name, contact/pager, primary and backup, deployment window (with time zone), explicit acknowledgement, and escalation timing in the team's approved change record. Share that record with all participants. SRE and Release Owner sign the readiness report against the exact image digest and evidence links. The current status is **no sign-off**.
