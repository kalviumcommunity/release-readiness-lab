# Dependency Checks

This file documents dependency verification and known vulnerabilities.

Current state
- `app/requirements.txt` pins `Flask==3.0.2`, `gunicorn==22.0.0`, `pytest==8.0.2`.
- Container base image uses `python:3.11-slim` in `app/Dockerfile` (consider pinning digest for production).

Suggested checks

1) Application dependencies

```bash
cd app
pip install -r requirements.txt
pip-audit > ../release-readiness-pack/evidence/pip-audit.txt || true
```

2) Container image scan

```bash
docker build -t myapp:canary -f app/Dockerfile app | tee release-readiness-pack/evidence/docker-build.log
trivy image --severity HIGH,CRITICAL -q -f json -o release-readiness-pack/evidence/trivy.json myapp:canary || true
```

Checklist
- [ ] All runtime dependencies pinned (application)
- [ ] Base image pinned or digest recorded
- [ ] No high/critical vulnerabilities in image (or mitigations documented)
