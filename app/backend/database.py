"""SQLite setup, migrations, demo identities, and health checks for GlobalBites."""

from __future__ import annotations

import os
import sqlite3
from pathlib import Path
from typing import Optional

from werkzeug.security import generate_password_hash

BACKEND_DIR = Path(__file__).resolve().parent
DEFAULT_DB_PATH = BACKEND_DIR / "data" / "globalbites.db"

DEMO_DINER = {
    "full_name": "Demo Diner",
    "email": "demo@globalbites.local",
    "phone": "70123456",
    "country_code": "+961",
    "password": "Demo123!",
    "role": "DINER",
}

DEMO_STAFF = {
    "full_name": "Demo Restaurant Staff",
    "email": "staff@globalbites.local",
    "phone": "70123457",
    "country_code": "+961",
    "password": "Staff123!",
    "role": "STAFF",
}


def get_db_path() -> str:
    return os.getenv("GLOBALBITES_DB_PATH", str(DEFAULT_DB_PATH))


def get_db_connection() -> sqlite3.Connection:
    path = Path(get_db_path())
    path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(path, timeout=10)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def _column_names(conn: sqlite3.Connection, table: str) -> set[str]:
    return {row["name"] for row in conn.execute(f"PRAGMA table_info({table})")}


def init_database(seed_demo: bool = True) -> None:
    """Create/migrate the local schema. Safe to call on every startup."""
    with get_db_connection() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                full_name TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                phone TEXT NOT NULL,
                country_code TEXT NOT NULL,
                password_hash TEXT NOT NULL,
                role TEXT NOT NULL DEFAULT 'DINER',
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            )
            """
        )

        if "role" not in _column_names(conn, "users"):
            conn.execute("ALTER TABLE users ADD COLUMN role TEXT NOT NULL DEFAULT 'DINER'")

        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS reservations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                restaurant_id INTEGER NOT NULL,
                restaurant_name TEXT NOT NULL,
                restaurant_cuisine TEXT NOT NULL,
                restaurant_location TEXT NOT NULL,
                reservation_date TEXT NOT NULL,
                reservation_time TEXT NOT NULL,
                guests INTEGER NOT NULL,
                table_code TEXT NOT NULL,
                seating_type TEXT NOT NULL,
                full_name TEXT NOT NULL,
                email TEXT NOT NULL,
                phone TEXT NOT NULL,
                status TEXT NOT NULL,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL,
                FOREIGN KEY (user_id) REFERENCES users(id)
            )
            """
        )
        conn.execute(
            """
            CREATE INDEX IF NOT EXISTS idx_reservation_slot
            ON reservations (restaurant_id, reservation_date, reservation_time, table_code, status)
            """
        )
        conn.execute(
            """
            CREATE UNIQUE INDEX IF NOT EXISTS uq_active_reservation_slot
            ON reservations (restaurant_id, reservation_date, reservation_time, table_code)
            WHERE status IN ('PENDING', 'CONFIRMED')
            """
        )
        conn.execute(
            """
            CREATE INDEX IF NOT EXISTS idx_reservation_user
            ON reservations (user_id, reservation_date)
            """
        )

        if seed_demo:
            for demo in (DEMO_DINER, DEMO_STAFF):
                existing = conn.execute(
                    "SELECT id FROM users WHERE email = ?", (demo["email"],)
                ).fetchone()
                if not existing:
                    conn.execute(
                        """
                        INSERT INTO users (
                            full_name, email, phone, country_code, password_hash, role
                        ) VALUES (?, ?, ?, ?, ?, ?)
                        """,
                        (
                            demo["full_name"],
                            demo["email"],
                            demo["phone"],
                            demo["country_code"],
                            generate_password_hash(demo["password"]),
                            demo["role"],
                        ),
                    )


def database_health() -> tuple[bool, Optional[str]]:
    try:
        with get_db_connection() as conn:
            conn.execute("SELECT 1").fetchone()
            conn.execute("SELECT COUNT(*) FROM users").fetchone()
        return True, None
    except Exception as exc:  # operational health surface
        return False, str(exc)


if __name__ == "__main__":
    init_database()
    print(f"GlobalBites database initialized at {get_db_path()}")
