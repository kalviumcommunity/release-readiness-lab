# Validation Results

## Scope

This validation pack records the evidence for the `v2.4` release candidate of the Checkout API.

## CI / Build Evidence

The repository CI workflow is defined in `.github/workflows/ci.yml` and performs the following checks:

- Python 3.11 setup
- `pip install -r app/requirements.txt`
- syntax validation with `python -m py_compile app/app.py app/test_app.py`
- `pytest app/test_app.py`
- Docker build as a dry-run image build with `docker/build-push-action@v5`

## Local Validation Commands Executed

```text
Set-Location 'c:\Users\joshu\OneDrive\Desktop\My files\programming\programs\Kalvium\release-readiness-lab\app'
..\.venv\Scripts\python.exe -m pytest -q
```

Observed output:

```text
..                                                                       [100%]
2 passed in 1.59s
```

```text
Set-Location 'c:\Users\joshu\OneDrive\Desktop\My files\programming\programs\Kalvium\release-readiness-lab\app'
..\.venv\Scripts\python.exe -m py_compile app.py test_app.py
```

Observed output:

```text
py_compile OK
```

## Runtime Validation Evidence

A live local runtime exercise was performed against Flask endpoints.

Observed output from the app startup and endpoint requests:

```text
2026-07-31 09:48:26,244 [INFO] checkout-api: Starting checkout-api vv2.4 on port 5000
 * Running on all addresses (0.0.0.0)
 * Running on http://127.0.0.1:5000
2026-07-31 09:48:27,267 [INFO] checkout-api: Handling request at / endpoint
2026-07-31 09:48:27,592 [WARNING] checkout-api: DATABASE_URL is not set! Using unstable, volatile in-memory SQLite fallback.
2026-07-31 09:48:27,593 [WARNING] checkout-api: REDIS_URL is not set! Using volatile local in-memory dict cache fallback.
2026-07-31 09:48:27,594 [INFO] werkzeug: 127.0.0.1 - - [31/Jul/2026 09:48:27] "GET /health HTTP/1.1" 200 -
```

The HTTP responses observed were:

- `/` => `200` with service metadata
- `/health` => `200` with `status: healthy` and fallback warnings

## Validation Summary

- Functional unit validation: PASS
- Syntax validation: PASS
- Runtime HTTP validation: PASS
- Production configuration presence: FAIL / incomplete
- Dependency vulnerability scan status: requires remediation

## Open Validation Gaps

- Docker build verification could not be completed in the workspace because Docker Desktop daemon access was unavailable.
- Kubernetes deployment validation was not executed in a cluster.
- Production config dependencies (`DATABASE_URL`, `REDIS_URL`) were not present in the target manifest and therefore not operationally proven.
