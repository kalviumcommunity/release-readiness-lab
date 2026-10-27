# Dependency checks

## Results

`app/requirements.txt` now pins all direct dependencies exactly:

```text
Flask==3.1.3
gunicorn==23.0.0
pytest==9.0.3
```

The original pins (`Flask==3.0.2`, `pytest==8.0.2`) were audited and reported known vulnerabilities (`PYSEC-2026-2151` and `PYSEC-2026-1845`). They were upgraded and reinstalled. The resulting command `python -m pip_audit -r requirements.txt` returned `No known vulnerabilities found` on 2026-10-27.

The runtime alignment is otherwise correct: `docs/architecture.md` requires Python 3.11, Flask 3.0.2+, and Gunicorn 22.0.0+; the Dockerfile uses Python 3.11 slim. CI must still confirm the updated set on Python 3.11. Transitive packages are resolved by pip and should be lockfile/SBOM-managed in the deployment pipeline.
