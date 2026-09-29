"""Deterministic reservation rules and persistence for GlobalBites."""

from __future__ import annotations

from datetime import date, datetime, timezone
import sqlite3

from .catalog import ACTIVE_RESERVATION_STATUSES, ALLOWED_TIMES, RESTAURANTS, TABLES
from .database import get_db_connection


class ReservationError(Exception):
    def __init__(self, message: str, status_code: int = 400):
        super().__init__(message)
        self.message = message
        self.status_code = status_code


def _parse_date(value: str) -> date:
    try:
        parsed = date.fromisoformat(value)
    except (TypeError, ValueError):
        raise ReservationError("Reservation date must use YYYY-MM-DD format.")
    if parsed < date.today():
        raise ReservationError("Reservation date cannot be in the past.")
    return parsed


def _normalize_creation(data: dict) -> dict:
    try:
        restaurant_id = int(data.get("restaurant_id"))
    except (TypeError, ValueError):
        raise ReservationError("A valid restaurant is required.")
    restaurant = RESTAURANTS.get(restaurant_id)
    if not restaurant:
        raise ReservationError("Restaurant not found.", 404)

    reservation_date = str(data.get("date") or "").strip()
    _parse_date(reservation_date)

    reservation_time = str(data.get("time") or "").strip()
    if reservation_time not in ALLOWED_TIMES:
        raise ReservationError("The selected reservation time is not supported.")

    try:
        guests = int(data.get("guests"))
    except (TypeError, ValueError):
        raise ReservationError("Guest count must be a number.")
    if guests < 1 or guests > 4:
        raise ReservationError("Guest count must be between 1 and 4 for the available tables.")

    table_code = str(data.get("table") or "").strip().upper()
    table = TABLES.get(table_code)
    if not table:
        raise ReservationError("A valid table is required.")
    if guests > table["capacity"]:
        raise ReservationError(
            f"Table {table_code} supports at most {table['capacity']} guests."
        )

    seating_type = str(data.get("seating_type") or "").strip().lower()
    if seating_type != table["seating_type"]:
        raise ReservationError("Table and seating type do not match.")

    return {
        "restaurant_id": restaurant_id,
        "restaurant": restaurant,
        "date": reservation_date,
        "time": reservation_time,
        "guests": guests,
        "table": table_code,
        "seating_type": seating_type,
    }


def create_reservation(user: dict, data: dict) -> dict:
    if user.get("role") != "DINER":
        raise ReservationError("Only diner accounts may create reservations.", 403)

    normalized = _normalize_creation(data or {})
    now = datetime.now(timezone.utc).isoformat()
    phone = f"{user['country_code']} {user['phone']}".strip()

    with get_db_connection() as conn:
        conflict = conn.execute(
            """
            SELECT id FROM reservations
            WHERE restaurant_id = ?
              AND reservation_date = ?
              AND reservation_time = ?
              AND table_code = ?
              AND status IN ('PENDING', 'CONFIRMED')
            """,
            (
                normalized["restaurant_id"],
                normalized["date"],
                normalized["time"],
                normalized["table"],
            ),
        ).fetchone()
        if conflict:
            raise ReservationError("That table is already reserved for the selected slot.", 409)

        try:
            cursor = conn.execute(
                """
                INSERT INTO reservations (
                    user_id, restaurant_id, restaurant_name, restaurant_cuisine,
                    restaurant_location, reservation_date, reservation_time, guests,
                    table_code, seating_type, full_name, email, phone, status,
                    created_at, updated_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 'PENDING', ?, ?)
                """,
                (
                    user["id"],
                    normalized["restaurant_id"],
                    normalized["restaurant"]["name"],
                    normalized["restaurant"]["cuisine"],
                    normalized["restaurant"]["location"],
                    normalized["date"],
                    normalized["time"],
                    normalized["guests"],
                    normalized["table"],
                    normalized["seating_type"],
                    user["full_name"],
                    user["email"],
                    phone,
                    now,
                    now,
                ),
            )
        except sqlite3.IntegrityError as exc:
            raise ReservationError(
                "That table is already reserved for the selected slot.", 409
            ) from exc
        row = conn.execute("SELECT * FROM reservations WHERE id = ?", (cursor.lastrowid,)).fetchone()
    return _serialize(row)


def list_reservations(user: dict) -> list[dict]:
    with get_db_connection() as conn:
        if user.get("role") == "STAFF":
            rows = conn.execute(
                "SELECT * FROM reservations ORDER BY reservation_date, reservation_time, id"
            ).fetchall()
        else:
            rows = conn.execute(
                """
                SELECT * FROM reservations
                WHERE user_id = ?
                ORDER BY reservation_date, reservation_time, id
                """,
                (user["id"],),
            ).fetchall()
    return [_serialize(row) for row in rows]


def availability(restaurant_id, reservation_date, reservation_time) -> dict:
    try:
        restaurant_id = int(restaurant_id)
    except (TypeError, ValueError):
        raise ReservationError("A valid restaurant is required.")
    if restaurant_id not in RESTAURANTS:
        raise ReservationError("Restaurant not found.", 404)
    reservation_date = str(reservation_date or "").strip()
    _parse_date(reservation_date)
    reservation_time = str(reservation_time or "").strip()
    if reservation_time not in ALLOWED_TIMES:
        raise ReservationError("The selected reservation time is not supported.")

    with get_db_connection() as conn:
        rows = conn.execute(
            """
            SELECT table_code FROM reservations
            WHERE restaurant_id = ?
              AND reservation_date = ?
              AND reservation_time = ?
              AND status IN ('PENDING', 'CONFIRMED')
            """,
            (restaurant_id, reservation_date, reservation_time),
        ).fetchall()
    booked = sorted({row["table_code"] for row in rows})
    available_tables = [code for code in TABLES if code not in booked]
    return {"booked": booked, "available": available_tables}


def transition_reservation(user: dict, reservation_id: int, requested_status: str) -> dict:
    requested_status = str(requested_status or "").strip().upper()
    with get_db_connection() as conn:
        row = conn.execute("SELECT * FROM reservations WHERE id = ?", (reservation_id,)).fetchone()
        if not row:
            raise ReservationError("Reservation not found.", 404)

        current = row["status"]
        owner = row["user_id"] == user["id"]
        role = user.get("role")

        if role == "DINER":
            if not owner:
                raise ReservationError("You are not authorized to change this reservation.", 403)
            if requested_status != "CANCELLED":
                raise ReservationError(
                    "Only restaurant staff may perform that lifecycle action.", 403
                )
            valid = current in {"PENDING", "CONFIRMED"}
        elif role == "STAFF":
            valid = (
                (current == "PENDING" and requested_status == "CONFIRMED")
                or (current == "CONFIRMED" and requested_status == "COMPLETED")
                or (current in {"PENDING", "CONFIRMED"} and requested_status == "CANCELLED")
            )
        else:
            raise ReservationError("Unknown account role.", 403)

        if not valid:
            raise ReservationError(
                f"Invalid transition from {current} to {requested_status}."
            )

        now = datetime.now(timezone.utc).isoformat()
        conn.execute(
            "UPDATE reservations SET status = ?, updated_at = ? WHERE id = ?",
            (requested_status, now, reservation_id),
        )
        updated = conn.execute("SELECT * FROM reservations WHERE id = ?", (reservation_id,)).fetchone()
    return _serialize(updated)


def _serialize(row) -> dict:
    return {
        "id": row["id"],
        "userId": row["user_id"],
        "restaurantId": row["restaurant_id"],
        "restaurantName": row["restaurant_name"],
        "restaurantCuisine": row["restaurant_cuisine"],
        "restaurantLocation": row["restaurant_location"],
        "date": row["reservation_date"],
        "time": row["reservation_time"],
        "guests": row["guests"],
        "table": row["table_code"],
        "seatingType": row["seating_type"],
        "fullName": row["full_name"],
        "email": row["email"],
        "phone": row["phone"],
        "status": row["status"],
        "createdAt": row["created_at"],
        "updatedAt": row["updated_at"],
    }
