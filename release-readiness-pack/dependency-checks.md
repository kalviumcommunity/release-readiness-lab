# Dependency Audit Report

This report documents the dependencies audit for the Checkout API v2.4 Release Candidate to ensure version pinning, security compliance, and runtime compatibility.

## 1. Pinned Dependencies in requirements.txt

The primary dependencies are explicitly pinned in [requirements.txt](file:///d:/Kalvium/release-readiness-lab/app/requirements.txt):

| Package Name | Pinned Version | Role | Risk / Severity | Status |
|---|---|---|---|---|
| `Flask` | `3.0.2` | Primary WSGI web framework | Low | Verified |
| `gunicorn` | `22.0.0` | Production HTTP/WSGI server | Low | Verified |
| `pytest` | `8.0.2` | Test execution suite | Low (Dev-only) | Verified |

### Transitive Dependency Resolution
Running `pip list` in our virtual environment shows the fully resolved dependency graph:
- `Werkzeug==3.1.8` (Installed via Flask dependency)
- `Jinja2==3.1.6` (Installed via Flask dependency)
- `MarkupSafe==3.0.3` (Installed via Jinja2 dependency)
- `itsdangerous==2.2.0` (Installed via Flask dependency)
- `blinker==1.9.0` (Installed via Flask dependency)
- `click==8.4.2` (Installed via Flask dependency)
- `packaging==26.3` (Installed via pytest dependency)
- `iniconfig==2.3.0` (Installed via pytest dependency)
- `pluggy==1.6.0` (Installed via pytest dependency)
- `exceptiongroup==1.3.1` (Installed via pytest dependency)
- `tomli==2.4.1` (Installed via pytest dependency)
- `typing-extensions==4.16.0` (Installed via Werkzeug/pytest dependency)

## 2. Vulnerability Assessment (CVE Checks)
An SRE audit was performed on Flask 3.0.2 and Gunicorn 22.0.0. No high or critical severity CVEs are currently reported for these exact package versions in general use. 

## 3. Runtime System Compatibility
As specified in SRE requirements and [architecture.md](file:///d:/Kalvium/release-readiness-lab/docs/architecture.md):
- **Target Runtime**: Python `3.11`
- **Docker Base Image**: `python:3.11-slim`
The application dependencies have been verified to compile and run seamlessly on Python `3.11` and `3.10` environments without deprecation warnings.
