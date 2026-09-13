# Dependency audit

Audit date: 2026-09-13. Python 3.11 matches `docs/architecture.md`, CI and the Docker base image's 3.11 series. Direct application dependencies are exactly pinned in `app/requirements.txt`.

| Package | Before | After | Reason |
| --- | --- | --- | --- |
| Flask | 3.0.2 | 3.1.3 | `pip-audit` reported `PYSEC-2026-2151`, fixed in 3.1.3 |
| Gunicorn | 22.0.0 | 22.0.0 | Version matches architecture; no advisory in the scan |
| pytest | 8.0.2 | 9.0.3 | `pip-audit` reported `PYSEC-2026-1845`, fixed in 9.0.3; test-only package |

Baseline command `pip-audit -r app/requirements.txt --progress-spinner off` reported four rows for two advisory/package pairs (each repeated). After upgrading, the same command reported `No known vulnerabilities found`. `pip check` reported no broken requirements; all four tests passed. This is a point-in-time advisory check, not proof of absence of unknown flaws.

Residual dependency gaps: transitive packages are resolved by version ranges rather than a full lockfile; `python:3.11-slim` is a mutable base tag; and `kalvium/checkout-api:v2.4` is not pinned by digest. Record a resolved package lock/SBOM, base image digest, and released image digest before production approval. The external PostgreSQL and Redis versions and compatibility have not been verified in a target environment.
