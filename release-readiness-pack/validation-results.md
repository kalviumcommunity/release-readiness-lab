# Validation Results

This file records the validation evidence (CI/build/test) gathered for the deployment candidate.

Summary
- CI status: NOT RUN (instructions below)
- Container build: NOT RUN
- Unit tests: NOT RUN
- Integration tests: NOT RUN

How to reproduce locally (run in repo root):

```bash
# Run the project's test suite (example - adapt to repo)
python -m pytest app/test_app.py | tee release-readiness-pack/evidence/unit-tests.txt || true

# Build container image
docker build -t myapp:canary -f app/Dockerfile app | tee release-readiness-pack/evidence/docker-build.log || true

# Run basic container smoke test
docker run --rm -e PORT=5000 -p 5000:5000 myapp:canary sh -c 'sleep 1; curl -fsS http://localhost:5000/health' | tee release-readiness-pack/evidence/smoke.txt || true

# Run k8s manifests in kind (recommended)
# kind create cluster
# kubectl apply -f k8s/
# kubectl wait --for=condition=available deployment/checkout-api --timeout=120s -n checkout-system
# kubectl logs deploy/checkout-api -n checkout-system --tail=100
```

Attach CI logs / screenshots here after running CI. Example filename suggestions:
- `release-readiness-pack/evidence/ci-build.log`
- `release-readiness-pack/evidence/unit-tests.txt`
- `release-readiness-pack/evidence/integration-tests.txt`

Notes / guidance
- The project's GitHub Actions CI is configured to run on `main` and PRs. Ensure the PR triggers the `validate` job which runs syntax checks, unit tests, and a dry-run Docker build.
- Add actual outputs under `release-readiness-pack/evidence/` and update the checklist below once each evidence item is collected.

Checklist
- [ ] CI build log committed
- [ ] Unit test report committed
- [ ] Integration test report committed
- [ ] Image pushed to registry with immutable tag
