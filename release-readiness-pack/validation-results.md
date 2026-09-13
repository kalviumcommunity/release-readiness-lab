# Validation results — checkout-api v2.4 candidate

Audit date: 2026-09-13. Source: `kalviumcommunity/release-readiness-lab` main at `ebe39e6`, plus this branch. Evidence was collected locally on Windows with Python 3.11.0; the repository CI targets Python 3.11 on Ubuntu.

Raw local command output: [local-validation.txt](./local-validation.txt).

| Check | Evidence | Result |
| --- | --- | --- |
| Python syntax | `.venv/Scripts/python -m py_compile app/app.py app/test_app.py` | Pass |
| Unit and negative configuration tests | `.venv/Scripts/python -m pytest app/test_app.py -q` → `4 passed in 0.11s` | Pass |
| Installed package consistency | `.venv/Scripts/python -m pip check` → `No broken requirements found.` | Pass |
| Dependency advisory scan | `pip-audit -r app/requirements.txt --progress-spinner off` → `No known vulnerabilities found` | Pass as of audit date |
| Kubernetes manifest parse and secret references | PyYAML parse of all three `k8s/*.yaml`; deployment requires both Secret keys | Pass, static only |
| Container build | [PR #9 CI run 34769086639](https://github.com/kalviumcommunity/release-readiness-lab/actions/runs/34769086639) completed successfully, including Docker Buildx dry-run image build | Pass in CI; image not published |
| Container startup | Docker daemon unavailable locally (`failed to connect to the docker API ... docker_engine`) | **Not verified** |
| In-cluster rollout, dependency connectivity and rollback | No production/staging cluster access or credentials available | **Not verified** |
| Branch CI | [PR #9 CI run 34769086639](https://github.com/kalviumcommunity/release-readiness-lab/actions/runs/34769086639), `validate` succeeded for branch commit `a5eda77` | Pass |

The original tests only checked that `/health` returned 200. New negative tests verify 503 when either required setting is absent. The successful test uses placeholder URLs and proves presence checking, **not** database or Redis connectivity.

CI includes syntax, unit tests and Docker build. The linked run validates this branch, but its dry-run build does not publish or sign an image. Record the immutable released image digest once available. No container startup or live dependency/rollback test is claimed.
