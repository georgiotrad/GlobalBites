# Final Requirements Matrix — GlobalBites

This maps the Operations Hub final rubric to GlobalBites without turning GlobalBites into a service-request product.

| Final requirement | GlobalBites implementation / evidence |
|---|---|
| Live entry | Flask/Gunicorn single-service deployment; `/login` exposes one-click demo diner and staff access. |
| Main user journey from UI | Browse restaurant -> booking form -> server availability -> create persisted reservation -> My Reservations. |
| Authorized internal work | Staff Dashboard confirms `PENDING` reservations and completes `CONFIRMED` reservations. |
| Boundary rejection | Backend rejects unauthenticated create, diner staff actions, invalid lifecycle transitions, over-capacity table, duplicate active slot, invalid date/time/table. |
| Updated state visible + persistent | Reservation pages read SQLite via API; no reservation/user authority in localStorage. Persistent-volume path is configurable. |
| Week 1 design | `docs/week1-design.md`. |
| Week 2 ownership | `docs/week2-engineering-ownership.md` + full-stack tests. |
| Week 3 full stack | Flask + HTML/JS + SQLite + sessions + integration-style Flask tests. |
| Week 4 production AI | Runtime decision-tree advisory, bounded inputs/output, safe failure, 8 ML evals, `docs/week4-production-ai.md`. |
| Week 5 release ownership | `railway.json`, `Procfile`, `.env.example`, `/api/health`, release SHA, logs, repeated monitor, release gate, smoke, failure/recovery doc. |
| Stranger user | Open live URL -> `/login` -> Demo Diner -> booking UI; Demo Staff -> Staff Dashboard. No Postman-only critical path. |
| Stranger engineer | Root README contains clone/install/config/init/run/test/eval/release/smoke instructions. |
| Operator | Health endpoint, release identity, logs, controlled ML failure, recovery, live smoke. |
| Exact release | `/api/health` surfaces `RELEASE_SHA` or platform commit environment variable. |
| Release gate | `python scripts/release_gate.py`. |
| Final smoke | `python scripts/smoke.py <live-url>`. |
| Final GO | Completion block in `docs/week5-release-ownership.md`. |
| Submission | `docs/submission-template.md`. |
| Defense | `docs/defense-checklist.md`. |

## External facts that cannot be pre-created in a ZIP

The following must be real and verified after Git/deployment:

1. Public repository URL.
2. Frozen final commit SHA.
3. Public live-app URL.
4. Platform logs from the deployed target.
5. Actual persistent-volume attachment confirmation.
6. Final live smoke output.
7. Final `GO` decision after all release checks pass.

Do not invent these values in advance.
