# Risk Analysis & Mitigation Matrix

This document provides a formal SRE risk assessment evaluating operational, security, and infrastructure risks associated with the deployment of the Checkout API v2.4 Release Candidate.

## Risk Assessment Framework
Risks are classified by:
- **Severity**: Critical / High / Medium / Low
- **Likelihood**: High / Medium / Low

---

## 1. Risk Matrix

| Risk ID | Description | Severity | Likelihood | Mitigation Strategy | Owner |
|---|---|---|---|---|---|
| **R-01** | **Volatile Fallback Execution**: Missing production `DATABASE_URL` and `REDIS_URL` causes application to use in-memory SQLite and local Dict cache, resulting in loss of state and session inconsistency. | Critical | High | Created [secret.yaml](file:///d:/Kalvium/release-readiness-lab/k8s/secret.yaml) containing Kubernetes secrets mapped to env vars in deployment manifests. | Lead SRE |
| **R-02** | **Credential Exposure**: Sensitive database and cache connection strings checked in as plain-text config or logs. | High | Medium | Enforce Kubernetes Opaque Secrets for credentials. ConfigMap only handles non-sensitive values (`LOG_LEVEL`, `PORT`). | SRE / DevOps |
| **R-03** | **Untested Rollback Execution**: Rollback procedures are documented but not tested under active load, resulting in extended downtime during incident. | High | Low | Dry-run the rollback procedure in the staging namespace. Document exact rollback instructions in [rollback-plan.md](file:///d:/Kalvium/release-readiness-lab/release-readiness-pack/rollback-plan.md). | Release Owner |
| **R-04** | **Unresolved Vulnerabilities (CVEs)**: Outdated Flask or Gunicorn packages containing unmitigated security vulnerabilities. | Medium | Low | Executed dependency audits and verified package pinning to secure versions in [dependency-checks.md](file:///d:/Kalvium/release-readiness-lab/release-readiness-pack/dependency-checks.md). | Security Lead |
| **R-05** | **Lack of Post-Deployment Verification**: Deployment finishes without checking actual HTTP status or connection status of dependencies. | Medium | Medium | Automated health probes defined in Deployment spec. Manual verification via Curl health commands included in the SRE checklist. | On-Call Engineer |

---

## 2. Risk Evaluation Conclusion
Prior to the remediation steps (namely introducing `secret.yaml` and securing the Deployment spec), the risk level was **CRITICAL** due to **R-01** and **R-02**. 
Following the mitigation steps, all identified risks have been brought down to acceptable operational thresholds (Medium / Low).
