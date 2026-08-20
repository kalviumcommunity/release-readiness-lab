# Operational Risk Analysis

This document catalogs and assesses the operational, security, and stability risks associated with the Checkout API v2.4 Release Candidate.

## 1. SRE Risk Evaluation Matrix

| Risk ID | Risk Description | Severity | Likelihood | Mitigation Plan | Owner |
|---|---|---|---|---|---|
| **RID-01** | **Vulnerable Web Framework**: `Flask 3.0.2` has known caching vulnerability `PYSEC-2026-2151` leaking private sessions. | **Medium** | **Medium** | Upgrade Flask to `3.1.3` (or later) and pin all transitive dependencies in `requirements.txt`. | SRE Lead |
| **RID-02** | **Missing DB / Redis Configs**: Connection strings omitted from `k8s/configmap.yaml` causing volatile fallbacks. | **High** | **High** | Inject `DATABASE_URL` and `REDIS_URL` into target environment config; update `k8s/configmap.yaml`. | Release Engineer |
| **RID-03** | **State Inconsistency (SQLite fallback)**: 3-pod replica setup writes to isolated in-memory RAM DBs, causing split-brain checkout data. | **High** | **High** | Never allow production rollout without verifying external Postgres and Redis connections. | Arch Lead |
| **RID-04** | **Dummy Health Check Probe**: `/health` endpoint only checks env string existence instead of actual downstream socket connectivity. | **High** | **Low** | Refactor Flask `/health` route to perform a real SQL query (`SELECT 1`) and a Redis `PING` command before returning `200 OK`. | Dev Team / SRE |
| **RID-05** | **Unpinned Docker Base Image**: Dockerfile base image specified as `python:3.11-slim`, which pulls the latest 3.11 patch on each build. | **Medium** | **High** | Pin the base image to a specific patch tag (`python:3.11.9-slim`) in the `Dockerfile`. | SRE Lead |
| **RID-06** | **Credential Exposure in ConfigMaps**: Database credentials are put in plain text inside `k8s/configmap.yaml`. | **Medium** | **Medium** | Migrate sensitive credentials to Kubernetes Secrets (`kind: Secret`) and reference them using `valueFrom.secretKeyRef`. | Security Eng |

---

## 2. Risk Mitigation & Resolution Details

### RID-01: Vulnerable Flask Web Framework
- **Impact**: Private session tokens and card processing details could be cached by edge CDN servers and served to random users.
- **Resolution**: Upgraded dependencies to `Flask==3.1.3` and `pytest==9.1.1`. Verified with `pip-audit` that the security footprint is completely clean.

### RID-02 & RID-03: Missing Configurations & SQLite Fallback
- **Impact**: The Checkout API handles checkout calculations, cart state, and payments. Ephemeral SQLite fallbacks mean cart calculations are lost during pod updates and fail when clients jump between replicas.
- **Resolution**: Updated `k8s/configmap.yaml` to configure target cluster service URLs. Release gate blocks deploy until target Postgres service is confirmed ready.

### RID-04: Dummy Health Check Probe
- **Impact**: Kubernetes will believe unhealthy pods are ready. If the database crashes, pods will report `healthy: true` to liveness probes, preventing Kubernetes from taking self-healing restart actions.
- **Resolution**: This remains an open code gap. Dev team must schedule a code improvement in the next sprint to add functional connectivity pings to the `/health` controller.

### RID-05: Unpinned Docker Base Image
- **Impact**: A future patch update to Python 3.11 could introduce breaking changes or different behaviors, leading to untraceable CI/CD build failures.
- **Resolution**: Updated the `Dockerfile` to pin `python:3.11.9-slim` to freeze the operating system and Python interpreter runtime.

### RID-06: Plain-Text Credentials in ConfigMaps
- **Impact**: Credentials checked into Git are visible to unauthorized developers and SRE logs.
- **Resolution**: Recommendation filed to move database URIs into a Kubernetes Secret.
