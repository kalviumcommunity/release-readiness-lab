# CI / Build / Validation Results

This document contains the validation evidence, local run logs, and unit test outputs for the Checkout API v2.4 Release Candidate.

## 1. Automated Test Summary

The unit tests run locally using `pytest` within the isolated python virtual environment.

### Test Execution Details
- **Python Version**: `3.10.11`
- **Pytest Version**: `8.0.2`
- **Execution Date/Time**: `2026-08-18 10:02:18 (Local)`
- **Host System**: Windows (Powershell Sandbox)

### Pytest Execution Log
```text
============================= test session starts =============================
platform win32 -- Python 3.10.11, pytest-8.0.2, pluggy-1.6.0
rootdir: D:\Kalvium\release-readiness-lab
collected 2 items

app\test_app.py ..                                                       [100%]

============================== 2 passed in 0.27s ==============================
```

## 2. Verified Test Cases

The following test suites located in [test_app.py](file:///d:/Kalvium/release-readiness-lab/app/test_app.py) were executed:

1. **`test_index`**: Verified that the root API endpoint returns status code `200`, specifies the service name as `checkout-api`, returns release candidate version `v2.4`, and returns the correct greeting.
2. **`test_health`**: Verified that the health check endpoint returns status code `200`, overall status `healthy`, and verifies the presence of database and redis cache check keys.

---
## 3. Container Validation
- **Dockerfile location**: [Dockerfile](file:///d:/Kalvium/release-readiness-lab/app/Dockerfile)
- **Base Image**: `python:3.11-slim` (Lightweight base, minimises vulnerability surface area)
- **Exposed Port**: `5000` (Redirected to Port `80` in Kubernetes cluster IP service)
- **Run Command**: Gunicorn WSGI server (`gunicorn --bind 0.0.0.0:5000 app:app`)
