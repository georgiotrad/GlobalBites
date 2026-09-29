"""Authentication domain logic for GlobalBites."""

from __future__ import annotations

import re
from typing import Optional

from werkzeug.security import check_password_hash, generate_password_hash

from .database import get_db_connection

EMAIL_PATTERN = re.compile(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$")


def validate_email(email: str | None) -> bool:
    return bool(email and EMAIL_PATTERN.match(email.strip()))


def validate_password(password: str | None) -> bool:
    return bool(password and len(password) >= 6)


def register_user(full_name, email, phone, country_code, password):
    full_name = (full_name or "").strip()
    email = (email or "").strip().lower()
    phone = (phone or "").strip()
    country_code = (country_code or "+961").strip()

    if len(full_name) < 2:
        return False, "Full name must be at least 2 characters", None
    if not validate_email(email):
        return False, "Invalid email format", None
    if not validate_password(password):
        return False, "Password must be at least 6 characters", None
    if not phone:
        return False, "Phone number is required", None

    try:
        with get_db_connection() as conn:
            if conn.execute("SELECT id FROM users WHERE email = ?", (email,)).fetchone():
                return False, "Email already registered", None
            cursor = conn.execute(
                """
                INSERT INTO users (
                    full_name, email, phone, country_code, password_hash, role
                ) VALUES (?, ?, ?, ?, ?, 'DINER')
                """,
                (full_name, email, phone, country_code, generate_password_hash(password)),
            )
            user_id = cursor.lastrowid
        return True, "Registration successful!", user_id
    except Exception:
        return False, "An error occurred during registration", None


def login_user(email, password):
    email = (email or "").strip().lower()
    if not validate_email(email):
        return False, "Invalid email format", None
    if not password:
        return False, "Password is required", None

    try:
        with get_db_connection() as conn:
            user = conn.execute("SELECT * FROM users WHERE email = ?", (email,)).fetchone()
        if not user or not check_password_hash(user["password_hash"], password):
            return False, "Invalid email or password", None
        return True, "Login successful!", _public_user(user)
    except Exception:
        return False, "An error occurred during login", None


def get_user_by_id(user_id) -> Optional[dict]:
    try:
        with get_db_connection() as conn:
            user = conn.execute("SELECT * FROM users WHERE id = ?", (user_id,)).fetchone()
        return _public_user(user) if user else None
    except Exception:
        return None


def get_user_by_email(email: str) -> Optional[dict]:
    try:
        with get_db_connection() as conn:
            user = conn.execute(
                "SELECT * FROM users WHERE email = ?", ((email or "").lower(),)
            ).fetchone()
        return _public_user(user) if user else None
    except Exception:
        return None


def _public_user(user) -> dict:
    return {
        "id": user["id"],
        "full_name": user["full_name"],
        "email": user["email"],
        "phone": user["phone"],
        "country_code": user["country_code"],
        "role": user["role"],
    }
