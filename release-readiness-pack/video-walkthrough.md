# 3–5 minute walkthrough guide

Record this as a screen share with your camera visible. Open the PR and show the actual code, evidence and report. Speak in your own words; the script below is a guide, not a substitute for the required recording.

**0:00–0:45 — Candidate gaps.** The v2.4 checkout API had a passing-code narrative but no release evidence pack. Its ConfigMap omitted database and Redis settings, while `/health` still returned 200. There was no verified rollback, named responder, risk register or approval.

**0:45–1:45 — Changes.** Show the seven pack files. Show the mandatory Secret references, deploy preflight, and `/health` returning 503 for missing settings. Show the upgraded Flask and pytest pins after the original audit found advisories. The architecture document now describes the required production configuration.

**1:45–2:45 — Evidence.** Show `local-validation.txt`: Python syntax passed, four tests passed, and `pip check` found no broken requirements. Show the dependency audit's repeated result of no known vulnerabilities and the linked PR CI run, including its Docker dry-run build. Explain that a placeholder URL in a unit test proves configuration presence only. Container startup and live connectivity remain unverified.

**2:45–3:45 — Recovery and risks.** Show the rollback runbook and stable v2.3 target from `docs/architecture.md`. Explain the need to verify its image digest and rehearse rollback before deployment. Show at least five risk rows and point out the open High risks: environment, rollback, ownership, image/rollout evidence and dependency health.

**3:45–4:30 — Decision.** Show `readiness-report.md`. State clearly: **NO-GO**. Local green tests are insufficient while any High risk remains open. List the evidence required to change the decision and note that no sign-off is recorded. End by showing the open PR URL.

Before submitting the video, upload it to Google Drive, set viewer access to “Anyone with the link,” and test the link in a private browser window. The student must appear visibly while explaining; a generated script alone does not meet that requirement.
