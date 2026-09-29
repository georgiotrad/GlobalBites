# Hard-Fail Prevention Checklist

Do not submit `GO` if any item below is true.

## Access
- repository is private/inaccessible or wrong;
- final SHA is unknown;
- no public live app;
- app depends on the student laptop;
- evaluator cannot enter with documented demo access.

## Product
- browser critical booking journey is broken;
- reservation flow works only through API tools;
- SQLite state is on an ephemeral filesystem;
- auth/authorization/validation is broken;
- ML advisory endpoint is broken in the final release.

## Evidence / operations
- release gate is red or not run;
- real secrets are committed;
- `/api/health` is missing/degraded at GO time;
- logs cannot be inspected;
- controlled failure has no recovery proof;
- live smoke is red.

## Ownership
- student cannot explain lifecycle rules, data model, ML boundary, persistence, health, failure/recovery, or remaining risk.
