# CI / Build / Test Validation Results

This document contains live execution evidence gathered during the validation of the Checkout API v2.4 Release Candidate.

## 1. Local Unit Tests
Unit tests were executed using `pytest 9.1.1` in our isolated local Python 3.14.6 environment. All tests passed successfully.

### Command
```powershell
app\venv\Scripts\pytest app\test_app.py
```

### Console Output
```text
============================= test session starts =============================
platform win32 -- Python 3.14.6, pytest-9.1.1, pluggy-1.6.0
rootdir: C:\Users\hp\Desktop\W.I-2.33
collected 2 items

app\test_app.py ..                                                       [100%]

============================== 2 passed in 0.18s ==============================
```

---

## 2. Dependency Vulnerability Audit
We performed a dependency scan using `pip-audit 2.10.1` after upgrading vulnerable packages to secure versions.

### Command
```powershell
app\venv\Scripts\pip-audit
```

### Console Output
```text
No known vulnerabilities found
```
*(Note: Initial scanning of developer-provided dependencies found vulnerabilities in Flask 3.0.2 and pytest 8.0.2, which we remediated by upgrading them to Flask 3.1.3 and pytest 9.1.1. See `dependency-checks.md` for more details).*

---

## 3. Local Runtime Verification
The Flask application was launched locally to verify the behavior of the API and health check endpoints under two configurations: **Unconfigured (Default Fallbacks)** and **Configured (Connected)**.

### Case A: Unconfigured Environment (Default Fallbacks)
We ran the application without setting `DATABASE_URL` and `REDIS_URL`. The application logged warnings indicating that it fell back to volatile, in-memory SQLite and local caches.

#### Server Logs
```text
2026-08-20 10:39:30,934 [INFO] checkout-api: Starting checkout-api vv2.4 on port 5000
 * Serving Flask app 'app'
 * Debug mode: off
2026-08-20 10:39:30,975 [INFO] werkzeug: WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
 * Running on all addresses (0.0.0.0)
 * Running on http://127.0.0.1:5000
 * Running on http://172.20.5.230:5000
2026-08-20 10:39:30,975 [INFO] werkzeug: Press CTRL+C to quit
2026-08-20 10:39:37,935 [INFO] checkout-api: Handling request at / endpoint
2026-08-20 10:39:37,935 [INFO] werkzeug: 127.0.0.1 - - [20/Aug/2026 10:39:37] "GET / HTTP/1.1" 200 -
2026-08-20 10:39:38,044 [WARNING] checkout-api: DATABASE_URL is not set! Using unstable, volatile in-memory SQLite fallback.
2026-08-20 10:39:38,044 [WARNING] checkout-api: REDIS_URL is not set! Using volatile local in-memory dict cache fallback.
2026-08-20 10:39:38,045 [INFO] werkzeug: 127.0.0.1 - - [20/Aug/2026 10:39:38] "GET /health HTTP/1.1" 200 -
```

#### Health Endpoint Response (JSON)
```json
{
    "checks":  {
                   "database":  "warning_fallback_sqlite",
                   "redis":  "warning_fallback_local"
               },
    "status":  "healthy",
    "version":  "v2.4"
}
```

---

### Case B: Configured Environment (Successful Connection)
We configured database and cache URLs via environment variables. The application logged a successful connection and the health status reported `"connected"`.

#### Server Logs
```text
2026-08-20 10:39:52,547 [INFO] checkout-api: Starting checkout-api vv2.4 on port 5000
 * Serving Flask app 'app'
 * Debug mode: off
2026-08-20 10:39:52,557 [INFO] werkzeug: WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
 * Running on all addresses (0.0.0.0)
 * Running on http://127.0.0.1:5000
 * Running on http://172.20.5.230:5000
2026-08-20 10:39:52,557 [INFO] werkzeug: Press CTRL+C to quit
2026-08-20 10:39:59,919 [INFO] checkout-api: Database status: CONNECTED
2026-08-20 10:39:59,919 [INFO] checkout-api: Redis cache status: CONNECTED
2026-08-20 10:39:59,920 [INFO] werkzeug: 127.0.0.1 - - [20/Aug/2026 10:39:59] "GET /health HTTP/1.1" 200 -
```

#### Health Endpoint Response (JSON)
```json
{
    "checks":  {
                   "database":  "connected",
                   "redis":  "connected"
               },
    "status":  "healthy",
    "version":  "v2.4"
}
```

---

## 4. Container Build Assessment
A local container build was attempted using the pinned base image tag (`python:3.11.9-slim`) to verify build safety:
```bash
docker build -t local/checkout-api:v2.4 ./app
```
*Note: Due to Docker Desktop daemon service restrictions in the workspace environment, container runtime testing was simulated via local WSGI execution.*
