# Dependency Checks

## Summary

`requirements.txt` already pins the direct runtime and test dependencies exactly:

- `Flask==3.0.2`
- `gunicorn==22.0.0`
- `pytest==8.0.2`

The Dockerfile also aligns with the architecture requirement by using `python:3.11-slim`.

## Evidence Collected

Local install verification:

```text
Successfully installed Flask-3.0.2 gunicorn-22.0.0 pytest-8.0.2
```

The dependency resolver also pulled compatible transitive packages such as Werkzeug, Jinja2, click, blinker, pluggy, and packaging.

## Assessment

| Check | Result | Notes |
|---|---|---|
| Direct dependency pinning | Pass | All top-level Python dependencies are exact-pinned versions. |
| Runtime base image alignment | Pass | Dockerfile uses Python 3.11, matching `docs/architecture.md`. |
| Test dependency availability | Pass | `pytest` installed and test suite executed successfully. |
| Supply-chain hardening | Partial | There is no lockfile or hash-locked constraints file, so installs rely on the package index at build time. |
| Host interpreter alignment | Partial | The local workstation ran Python 3.13.9, which is not the production target; production verification should rely on the Docker image/runtime. |

## Conclusion

The direct dependency set is appropriately pinned for this lab, but release approval should still require container-based validation under Python 3.11 and, ideally, hash-based lock enforcement for stronger supply-chain control.
