# Final Defense Checklist — GlobalBites

Have these ready in separate tabs/terminals:

## Live product
- Live app URL.
- `/login` demo access.
- Diner booking journey.
- Staff dashboard and valid lifecycle transition.
- Refresh to show persistence.

## Product and architecture
Explain the same-origin Flask architecture, SQLite persistent volume, session identity, server-owned restaurant/table catalog, and reservation state machine.

## Boundaries
Show one allowed action and one rejected action. Explain that browser data and ML output do not grant authority.

## Proof
Show submitted SHA, `python scripts/release_gate.py`, full-stack tests, 8 ML evals and live smoke.

## Operations
Show `/api/health`, platform logs, release SHA, controlled ML failure, recovery, and the critical path after recovery.

## Ownership questions
Be ready to explain why localStorage was removed for authoritative state, why SQLite needs persistent storage, how slot conflicts are prevented, why ML is advisory, what remains risky, and why the final release is GO.
