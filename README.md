# Release Readiness Lab: Checkout API (v2.4 Release Candidate)

Welcome to the Release Engineering / SRE Team!

This repository contains the code and configuration for the **Checkout API (v2.4 Release Candidate)**.

The development team has completed feature development, verified the application code, and successfully run the CI pipeline. They believe it is ready for immediate deployment to production and have handed it over to you.

However, as a Release Engineer or Site Reliability Engineer, you know that **"technically deployable" does not mean "operationally ready for production."** The repository is currently missing all critical operational verification artifacts, risk assessments, and governance plans.

Your task is to conduct a thorough release audit, gather execution evidence, analyze configuration settings, audit dependencies, establish operational ownership, create a rollback plan, and present a final **Go / No-Go** recommendation in a structured **Release Readiness Pack (RRP)**.

---

## Repository Structure

The workspace is organized as follows:

- [app/](./app/) - Contains the Flask application, Gunicorn configuration, dependencies, Dockerfile, and unit tests.
- [k8s/](./k8s/) - Contains the Kubernetes deployment, service, and configuration manifests.
- [scripts/](./scripts/) - Contains helper deployment scripts.
- [docs/](./docs/) - Architectural overview and release history.
- [release-readiness-pack/](./release-readiness-pack/) - The folder where your deliverables **must** be created.

---

## Release Governance Guidelines

You must compile a complete **Release Readiness Pack** inside the `release-readiness-pack/` directory. Your pack must contain the following documents (in Markdown format):

1. **Validation Report** (`validation-results.md`): Collect build, test, and containerization validation evidence (such as CI run outputs, local run validations, health check responses, etc.).
2. **Configuration Verification Checklist** (`config-verification.md`): Inspect `k8s/configmap.yaml` and `app/app.py`. Document configuration variables, identify fallbacks, and highlight missing production variables.
3. **Dependency Audit** (`dependency-checks.md`): Examine dependencies pinned in `requirements.txt`. Check for best-practice pinning, compile version reports, and verify they match runtime system requirements in `docs/architecture.md`.
4. **Rollback Plan** (`rollback-plan.md`): Prepare concrete steps to rollback if deployment fails in production. Identify the target stable rollback version based on repository documentation, write exact rollback commands, and define verification steps post-rollback.
5. **Risk Analysis** (`risk-analysis.md`): Create a risk matrix evaluating at least 5 operational risks (e.g., container security, missing configuration vars, single points of failure, rollback documentation). Classify them by severity, likelihood, mitigation, and owner.
6. **Deployment Ownership** (`ownership.md`): Define and document clear ownership roles (Release Owner, SRE/Operational Lead, On-Call Support, Escalation Path) to prevent "orphaned" deployments.
7. **Readiness Report & Go/No-Go Decision** (`readiness-report.md`): Synthesize all findings into a final report. Make an explicit, evidence-backed **Go** or **No-Go** recommendation with operational justification.

### How to Evaluate

Your submission will be evaluated on the completeness, professional formatting, and analytical quality of the artifacts in your `release-readiness-pack/` folder.

---

## Local Setup & Inspection

### Running Python App Locally

```bash
cd app
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python app.py
```

### Running Tests Locally

```bash
cd app
pytest test_app.py
```

### Simulating Kubernetes Deployment

To test manifests locally in Minikube, Kind, or Docker Desktop:

```bash
chmod +x scripts/deploy.sh
./scripts/deploy.sh
```
