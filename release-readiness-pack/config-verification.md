# Configuration & Environment Verification

This file documents verification of environment, configuration, and secrets for the target production environment.

Checklist
- [ ] Confirmed required environment variables are defined for production
- [ ] Secrets stored in approved secret store (Vault/Secrets Manager)
- [ ] Kubernetes manifests do not contain plaintext secrets
- [ ] Resource requests & limits set for pods
- [ ] Health/readiness probes present
- [ ] Config maps / feature flags validated

Expected variables (based on app):
- `DATABASE_URL` — required for stable DB connections (production)
- `REDIS_URL` — required for distributed cache in production
- `LOG_LEVEL`

Verification commands (run from repo root):

```bash
# Check k8s manifests for plaintext secrets
grep -R "password\|secret\|AWS_SECRET" -n k8s || true

# Show missing env var placeholders in manifests
grep -R "${" -n k8s || true

# Validate resource requests/limits
grep -R "resources:" -n k8s || true

# Verify probes
grep -R "readinessProbe\|livenessProbe" -n k8s || true
```

How to record evidence:
- Save the outputs above to `release-readiness-pack/evidence/config-checks.txt`.
- If secrets are in plaintext in manifests, record file and line in `config-verification.md` and remediate before production.

Notes / recommended remediation
- The current `k8s/configmap.yaml` intentionally omits `DATABASE_URL` and `REDIS_URL`, causing the app to use volatile fallbacks — this is unacceptable for production. Add these secrets to a Secret store and reference them as environment variables or use external secret management.
