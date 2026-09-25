release-readiness-pack/dependency-checks.md

# Dependency Verification & Vulnerability Scan

## Pinned Dependencies
nginx: alpine (Image Digest pinned in deployment spec)
Base Node/Python packages pinned in package-lock.json / requirements.txt

## Security Audit Output
text
$ npm audit
found 0 vulnerabilities

$ trivy image nginx:alpine
Total: 0 (UNKNOWN: 0, LOW: 0, MEDIUM: 0, HIGH: 0, CRITICAL: 0)

---