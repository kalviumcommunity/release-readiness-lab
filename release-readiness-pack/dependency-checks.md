# Dependency Checks

## Pinned Runtime Requirements

The application dependencies are pinned in `app/requirements.txt`:

```text
Flask==3.1.3
gunicorn==22.0.0
pytest==9.0.3
```

These versions are exact pins, which is a positive production practice.

## Verification Evidence

A dependency consistency check was run with:

```text
.\.venv\Scripts\python.exe -m pip check
```

Observed output:

```text
No broken requirements found.
```

A vulnerability scan was run with:

```text
.\.venv\Scripts\python.exe -m pip_audit -r app/requirements.txt
```

Observed output:

```text
Found 2 known vulnerabilities in 2 packages
Name   Version ID              Fix Versions
------ ------- --------------- ------------
flask  3.0.2   PYSEC-2026-2151 3.1.3
pytest 8.0.2   PYSEC-2026-1845 9.0.3
```

## Remediation Applied

The pinned versions were updated to remediate the known vulns by moving to:

- `Flask==3.1.3`
- `pytest==9.0.3`

## Remaining Review Items

- Runtime compatibility must be confirmed against the production Python 3.11 target.
- The Docker image should be rebuilt and scanned in the actual CI pipeline or release environment.
- `gunicorn==22.0.0` is pinned, but it should be validated in the target container runtime.
