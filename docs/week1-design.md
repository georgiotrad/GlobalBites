# Week 1 — Design Evidence

## Product problem
GlobalBites helps diners discover restaurants and reserve tables. The critical final-capstone journey is a diner selecting a restaurant and available slot, persisting a reservation, and an authorized restaurant staff actor advancing that reservation through its lifecycle.

## Actors
- **Diner**: register/login, browse, inspect availability, create a reservation, view own persisted reservations, cancel own active reservation.
- **Restaurant Staff**: view all persisted reservations and perform staff lifecycle actions.
- **ML advisory**: predicts outdoor demand from bounded weather inputs; it is not an actor with business authority.

## Architecture decision
A single-origin Flask application serves HTML/CSS/JS and JSON APIs. SQLite provides persistence. Gunicorn is the production WSGI process. This deliberately avoids unnecessary microservices and CORS complexity.

## Core data model
`users`: identity, contact details, password hash, role.

`reservations`: user ownership, restaurant snapshot, date/time, guest count, table, seating type, status, created/updated timestamps.

The restaurant catalog and table capacities are product-owned constants in `app/backend/catalog.py`; server validation never trusts browser labels or restaurant metadata.

## Reservation state model
`PENDING` -> `CONFIRMED` -> `COMPLETED`

Active reservations may transition to `CANCELLED` under role/ownership rules.

## Decisions
1. Reservation state is authoritative in SQLite, not localStorage.
2. Passwords are stored only as Werkzeug hashes.
3. Demo roles use server sessions; browser role labels do not grant authority.
4. Table availability is deterministic and based on active persisted rows.
5. ML is advisory and isolated from reservation authority.
6. A persistent deployment volume is required for SQLite.
