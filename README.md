# GlobalBites — AI Academy Final Capstone

GlobalBites is a full-stack restaurant discovery and reservation application upgraded to the same Week 1–5 engineering standard used for the Internal Operations Service Hub capstone. It keeps the original restaurant product, Flask architecture, SQLite persistence, and outdoor-demand ML model, while adding deterministic reservation authority, demo roles, cumulative evidence, automated proof, and release ownership.

## Live handoff

Fill these only after the repository is pushed and the real deployment is verified:

- Repository URL: `TBD_AFTER_PUSH`
- Final frozen commit SHA: `TBD_AFTER_FINAL_COMMIT`
- Live App URL: `TBD_AFTER_DEPLOYMENT`
- Health URL: `TBD_AFTER_DEPLOYMENT/api/health`

### Demo access

Open `/login` and use either one-click identity:

- **Demo Diner** — creates reservations, sees only its own reservations, and may cancel its own active reservations.
- **Demo Restaurant Staff** — sees all persisted reservations and may perform staff lifecycle actions.

Seeded credentials are also available for manual login:

- Diner: `demo@globalbites.local` / `Demo123!`
- Staff: `staff@globalbites.local` / `Staff123!`

These are intentionally non-secret demo accounts. Do not reuse them for real users.

## Critical live journey

1. Open the live URL and choose **Demo Diner Access**.
2. Browse restaurants and open a restaurant.
3. Choose **Book a Table**.
4. Select a future date, supported time, number of guests, and an available table.
5. Submit the reservation. The backend assigns the identity, restaurant metadata, initial `PENDING` state, timestamps, and persists the row in SQLite.
6. Open **My Reservations** and verify the same persisted reservation is visible.
7. Log out, use **Demo Restaurant Staff Access**, and open the Staff Dashboard.
8. Confirm the `PENDING` reservation. The valid lifecycle transition succeeds and persists.
9. Try an invalid transition (for example `PENDING -> COMPLETED` through the API test suite) and verify rejection without state corruption.
10. Refresh/re-open the page and verify state remains visible.

## Reservation authority and lifecycle

The browser never decides reservation authority. The backend validates restaurant, date, time, guest count, table capacity, seating type, slot conflicts, authentication, ownership, role, and lifecycle.

Valid transitions:

- Diner: `PENDING -> CANCELLED`, `CONFIRMED -> CANCELLED` for their own reservation.
- Staff: `PENDING -> CONFIRMED`, `CONFIRMED -> COMPLETED`, and active reservation -> `CANCELLED`.

Invalid or unauthorized transitions are rejected and leave the persisted row unchanged.

## ML capability and boundary

The homepage uses the supplied decision-tree model (`outdoor_booking_model.pkl`) to estimate outdoor booking demand from bounded weather inputs. The output is an **advisory operational signal** only.

The ML model may recommend outdoor preparation. It may **not** decide:

- whether a table is available;
- whether a booking is accepted;
- which user owns a reservation;
- any reservation status transition;
- authorization;
- persisted database state.

Invalid inputs, invalid model output, missing model/provider failure, and prediction exceptions fail safely. The reservation system remains under deterministic software authority.

## Architecture

```text
Browser
  |
  | same-origin HTML/CSS/JS + JSON API
  v
Flask / Gunicorn
  |-- authentication/session boundary
  |-- reservation business rules
  |-- ML advisory endpoint
  |-- health/release endpoint
  v
SQLite persistent volume

ML endpoint -> scikit-learn DecisionTreeRegressor model
             (advisory only; never reservation authority)
```

## Local setup — stranger engineer test

Requirements: Python 3.11+ recommended.

```bash
python -m venv .venv
```

Activate it:

Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

macOS/Linux:

```bash
source .venv/bin/activate
```

Install:

```bash
pip install -r requirements.txt
```

Optional local environment variables:

```bash
# Windows PowerShell examples
$env:SECRET_KEY="local-development-secret"
$env:GLOBALBITES_DB_PATH="$PWD\app\backend\data\globalbites.db"
$env:RELEASE_SHA="local"
```

Run:

```bash
python -m app.backend.app
```

Open `http://127.0.0.1:5000`.

The schema and demo identities are initialized automatically. No committed database is required.

## Automated proof

Run all tests:

```bash
python -m pytest -q
```

Run the 8 representative ML evaluations:

```bash
python -m pytest -q tests/test_ml_eval.py
```

Run the complete release gate:

```bash
python scripts/release_gate.py
```

The release gate compiles the Python sources, runs the deterministic/integration tests, and runs the ML eval suite explicitly.

## Live smoke test

After deployment:

```bash
python scripts/smoke.py https://YOUR-LIVE-APP
```

The smoke checks health and ML, signs in as the demo diner, creates a real persisted reservation, switches to staff, confirms it, reads the persisted state, and then cancels it through a valid staff transition to release the active slot.

## Production configuration

Do not commit real secrets. Use platform environment variables:

- `SECRET_KEY` — long random secret for Flask sessions.
- `GLOBALBITES_DB_PATH` — path on the persistent volume, e.g. `/data/globalbites.db`.
- `RELEASE_SHA` — exact frozen Git SHA submitted to the academy.
- `SEED_DEMO_USERS=1` — keep enabled for the capstone defense/demo.
- `COOKIE_SECURE=1` — enable on HTTPS deployment.
- `GLOBALBITES_ML_FORCE_FAILURE=0` — normal operation; use `1` only for a controlled failure exercise.

A sample is provided in `.env.example`.

## Railway deployment

This repository includes `railway.json` and a `Procfile`.

Recommended single-service deployment:

1. Push the public repository.
2. Create a Railway service from the repository.
3. Mount a persistent volume at `/data`.
4. Set `GLOBALBITES_DB_PATH=/data/globalbites.db`.
5. Set `SECRET_KEY` to a generated secret.
6. Set `COOKIE_SECURE=1`.
7. Set `SEED_DEMO_USERS=1`.
8. Deploy with the included start command: `gunicorn app.backend.app:app --bind 0.0.0.0:$PORT`.
9. After choosing the final frozen commit, set `RELEASE_SHA` to that exact SHA and redeploy that SHA.
10. Verify `/api/health`, platform logs, the UI critical path, and `python scripts/smoke.py <live-url>`.

The SQLite file must be on the mounted persistent volume. A deployment using only an ephemeral filesystem does not satisfy the final persistence handoff.

## Health, logs, monitoring, and release identity

`GET /api/health` reports:

- overall `healthy` / `degraded` status;
- exact `release` identifier;
- SQLite check;
- ML-model check.

The app logs authentication events, reservation creation, lifecycle transitions, and unexpected server errors. The deployment platform's service logs are the operational log surface; no paid observability product is required.

For repeatable lightweight monitoring evidence:

```bash
python scripts/monitor.py https://YOUR-LIVE-APP 6 10
```

This performs six health observations ten seconds apart and fails if any observation is unhealthy.

## Controlled failure and recovery

Safe Week 5 demonstration for the ML dependency:

1. Confirm `/api/health` is healthy and run the live smoke.
2. Set `GLOBALBITES_ML_FORCE_FAILURE=1` and restart/redeploy.
3. `/api/health` becomes degraded and `/api/ml/predict` fails safely; no reservation database corruption is introduced.
4. Review deployment logs for the affected dependency.
5. Restore `GLOBALBITES_ML_FORCE_FAILURE=0` and restart/redeploy.
6. Confirm `/api/health` is healthy again.
7. Run the live smoke again and re-run the browser critical path.

This is a controlled dependency failure; do not delete or corrupt the persistent database to demonstrate failure.

## Cumulative Week 1–5 evidence

- `docs/week1-design.md`
- `docs/week2-engineering-ownership.md`
- `docs/week3-full-stack.md`
- `docs/week4-production-ai.md`
- `docs/week5-release-ownership.md`
- `docs/defense-checklist.md`
- `docs/submission-template.md`

## Final release procedure

1. Work on the final release branch.
2. Install from a clean environment.
3. Run `python scripts/release_gate.py`.
4. Push and deploy the exact candidate commit.
5. Verify `/api/health` reports the intended release.
6. Run `python scripts/smoke.py <live-url>`.
7. Perform the UI critical path as both demo roles.
8. Review logs and verify the SQLite volume is mounted.
9. Record remaining risk in `docs/week5-release-ownership.md`.
10. Decide `GO` only when all checks are green.
11. Record and submit the exact frozen commit SHA. Later pushes should not be treated as part of the submitted release unless the academy explicitly requests them.

## Original product assets

The restaurant catalog, images, design, weather dataset, and supplied ML model from the original GlobalBites project are retained. The final-capstone changes focus on engineering ownership, full-stack persistence, runtime ML boundaries, operational proof, and stranger handoff rather than replacing the restaurant product.

### Additional final-handoff evidence

- `docs/final-requirements-matrix.md` — requirement-by-requirement mapping.
- `docs/three-stranger-test.md` — stranger user / engineer / operator test.
- `docs/hard-fail-checklist.md` — final NO-GO baseline.
