# Risk Analysis

This document lists unresolved risks, their severity, likelihood, mitigation, and an assigned owner.

1) Missing end-to-end integration tests
- Severity: High
- Likelihood: High
- Impact: Regressions in production critical flows
- Mitigation: Run full E2E test suite in staging; block release until critical E2E pass or add targeted smoke tests and feature flags
- Owner: `qa-lead@example.com`

2) Unpinned / un-scanned dependencies
- Severity: High
- Likelihood: Medium
- Impact: Security vulnerabilities, runtime incompatibilities
- Mitigation: Pin all deps, run `pip-audit` and `trivy` on images; patch or mitigate before release
- Owner: `dev-owner@example.com`

3) Rollback untested
- Severity: High
- Likelihood: Medium
- Impact: Extended downtime if rollback fails
- Mitigation: Execute rollback plan in staging and record results; have SRE on-call during deploy window
- Owner: `sre-oncall@example.com`

4) Secrets in manifests / improper secret management
- Severity: Medium
- Likelihood: Low
- Impact: Credential leakage
- Mitigation: Move secrets to Vault/Secrets Manager, rotate exposed secrets, require PR gating checks
- Owner: `platform-security@example.com`

Risk Register Summary
- High risks blocking approval: Missing E2E tests, Unpinned deps, Rollback untested.
