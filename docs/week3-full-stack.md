# Week 3 — Full-Stack Evidence

## Integrated stack
- Frontend: existing GlobalBites HTML/CSS/JavaScript served by Flask.
- Backend: Flask JSON APIs and session boundary.
- Database: SQLite with automatic schema initialization/migration.

## Main integrated flow
The booking UI calls the backend availability endpoint, then `POST /api/reservations`. The backend derives user identity from the session and restaurant metadata from its trusted catalog. The My Reservations / Staff Dashboard page reads `GET /api/reservations` and lifecycle buttons call the status endpoint.

## Persistence
The browser no longer stores users or bookings in localStorage. Refreshing or opening a new browser request reads the authoritative SQLite state through the API.

## Security and errors
Passwords are hashed, SQL uses parameters, sessions use HttpOnly/SameSite cookies, and role/ownership checks execute on the backend. API failures return bounded messages; unexpected errors are logged and mapped to an API 500 response.

## Integration/E2E-style automated proof
Flask's test client exercises the actual routes, sessions, business layer and a temporary SQLite database. The release gate runs the suite from a clean command.
