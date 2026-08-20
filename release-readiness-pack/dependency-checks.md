# Dependency Audit & Version Checks

This document details the dependency analysis, version locking, security vulnerability scanning, and environment audit for the Checkout API service.

## 1. Initial Vulnerability Scan (Flask 3.0.2 & Pytest 8.0.2)
We audited the original developer-provided dependencies using `pip-audit 2.10.1`. The audit identified **2 known vulnerabilities** in the dependencies specified in the original `requirements.txt`:

| Package | Original Version | ID | Fix Version | Description / Threat Vector | Severity |
|---|---|---|---|---|---|
| `flask` | `3.0.2` | `PYSEC-2026-2151` | `3.1.3` | **Use of Cache Containing Sensitive Information**: Flask does not set `Vary: Cookie` when sessions are accessed via the `in` operator. Private user data may be cached on edge proxy servers (e.g., Cloudflare, Varnish) and exposed to other users. | Medium |
| `pytest` | `8.0.2` | `PYSEC-2026-1845` | `9.0.3` | **Insecure Temp Directory on Unix**: Predictable `/tmp/pytest-of-{user}` directories allow local attackers on shared machines to trigger DOS or escalate privileges. | Low (CI/CD risk) |

---

## 2. Dependency Remediation & Locking

To ensure operational stability and fix security vulnerabilities, we upgraded the vulnerable packages and pinned all transitive dependencies in [app/requirements.txt](file:///c:/Users/hp/Desktop/W.I-2.33/app/requirements.txt):

### remediated requirements.txt
```text
Flask==3.1.3
gunicorn==22.0.0
pytest==9.1.1
blinker==1.9.0
click==8.4.2
itsdangerous==2.2.0
Jinja2==3.1.6
MarkupSafe==3.0.3
Werkzeug==3.1.8
packaging==26.3
colorama==0.4.6
iniconfig==2.3.0
pluggy==1.6.0
pygments==2.21.0
```

### Post-Remediation Security Status
Scanning the updated environment with `pip-audit` returned:
```text
No known vulnerabilities found
```

---

## 3. System Target vs Runtime Environment Mismatch

The `docs/architecture.md` specifies strict system target requirements:
- **Target Python Version**: `3.11`
- **Current Runtime (Local/Test)**: `Python 3.14.6` (from SRE workspace tooling)

### SRE Assessment
1. **Target Discrepancy**: The local test environment runs Python 3.14.6, whereas production runs the container image on Python 3.11. Although unit tests passed, running tests on Python 3.14 does not guarantee absolute safety under Python 3.11.
2. **Action Item**: The Dockerfile has been updated to use `FROM python:3.11.9-slim` to enforce that the actual container runs on Python 3.11 in staging and production.
3. **CI/CD Lock**: We must configure the CI runner pipeline to execute Python tests using python `3.11` exclusively.
4. **Gunicorn System Context**: `gunicorn` is included in the requirements, but it is a WSGI server designed for Unix/Linux environments. It will fail to run natively on SRE Windows development workstations, requiring WSL or containerization for local production-simulation runs.
