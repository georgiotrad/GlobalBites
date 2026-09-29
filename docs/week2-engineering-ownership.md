# Week 2 — Engineering Ownership Evidence

## Lifecycle rules
- New diner reservation: `PENDING`.
- Staff: `PENDING -> CONFIRMED`.
- Staff: `CONFIRMED -> COMPLETED`.
- Diner: own `PENDING|CONFIRMED -> CANCELLED`.
- Staff: active `PENDING|CONFIRMED -> CANCELLED`.
- Any other transition is rejected.

## Validation rules
The backend validates authenticated identity, role, restaurant ID, supported date/time, no past date, guest range, table identity, table capacity, seating type, and active-slot conflict.

## Allowed proof
`tests/test_full_stack.py` proves creation, persistence, staff confirmation/completion, diner cancellation, and authenticated access.

## Rejected proof
The same suite proves duplicate-slot conflict, invalid lifecycle transition with unchanged state, unauthenticated create rejection, and capacity-rule rejection.

## Ownership method
- **UNDERSTAND**: the backend owns identity, lifecycle and availability.
- **DIRECT**: client requests intent only (`create`, `confirm`, `cancel`, etc.).
- **PROVE**: automated tests assert both success and rejection boundaries.
