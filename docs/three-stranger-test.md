# Three-Stranger Handoff Test

## Stranger user
Pass criteria:
- opens the public live URL;
- follows `/login` demo access without source edits;
- uses restaurant browsing and booking through the UI;
- sees the persisted reservation;
- can switch to demo staff and perform a valid staff transition;
- never needs localhost, Postman, a developer laptop, or undocumented setup.

## Stranger engineer
Pass criteria using the root README only:
- clone repository;
- create virtual environment;
- install `requirements.txt`;
- configure `.env.example` values as environment variables;
- run `python -m app.backend.app`;
- run `python -m pytest -q`;
- run `python -m pytest -q tests/test_ml_eval.py`;
- run `python scripts/release_gate.py`.

## Operator
Pass criteria:
- identify the deployed commit from `/api/health`;
- verify DB + ML dependency status;
- inspect service logs;
- demonstrate controlled ML failure using `GLOBALBITES_ML_FORCE_FAILURE=1`;
- recover by restoring configuration and restarting;
- run live smoke and the UI critical path again.
