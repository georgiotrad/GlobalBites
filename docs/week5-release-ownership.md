# Week 5 — Release Ownership Evidence

## Remote target
One public Flask/Gunicorn service serves frontend and API. SQLite must use a mounted persistent volume. Railway configuration is included; another host is acceptable only if equivalent persistence and environment configuration are provided.

## Required runtime configuration
- `SECRET_KEY`
- `GLOBALBITES_DB_PATH=/data/globalbites.db` (example persistent mount)
- `RELEASE_SHA=<frozen submitted SHA>`
- `SEED_DEMO_USERS=1`
- `COOKIE_SECURE=1`

Real secret values must never be committed.

## Release gate
`python scripts/release_gate.py`

GO requires compilation, all tests, the explicit ML eval suite, healthy live target, live smoke, UI critical path, logs review, and persistent storage verification.

## Health, signals, and repeated observation
`/api/health` reports release identity, database readiness and model readiness. Operational logs record login, reservation creation, transitions and unexpected server errors. `python scripts/monitor.py <live-url> 6 10` provides repeatable short-window monitoring evidence without requiring a paid observability service.

## Controlled failure
Set `GLOBALBITES_ML_FORCE_FAILURE=1`, restart, observe degraded health and safe ML failure, then restore `0`, restart and prove recovery with health + smoke + UI critical path.

## Recovery
No destructive database failure is required. For application failure: inspect logs, revert bad config/release, restart/redeploy, check health, run smoke, repeat critical path.

## Final smoke
`python scripts/smoke.py <live-url>` creates a demo reservation, performs a valid staff transition, proves persisted visibility, and cancels the row to release the active table.

## Final GO record
Complete this section before submission:
- Candidate SHA: `TBD`
- Live URL: `TBD`
- Release gate: `TBD PASS/FAIL`
- Health: `TBD`
- Smoke: `TBD PASS/FAIL`
- UI diner journey: `TBD PASS/FAIL`
- UI staff journey: `TBD PASS/FAIL`
- Persistent volume verified: `TBD YES/NO`
- Logs reviewed: `TBD YES/NO`
- Remaining risk: `TBD`
- Decision: `TBD GO/NO-GO`
