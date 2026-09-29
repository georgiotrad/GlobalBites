"""GlobalBites production-ready Flask application."""

from __future__ import annotations

import logging
import os
from pathlib import Path

from flask import Flask, jsonify, render_template, request, session

from .auth import get_user_by_email, get_user_by_id, login_user, register_user
from .database import DEMO_DINER, DEMO_STAFF, database_health, init_database
from .ml_system import PredictionInputError, model_health, predict_today
from .reservations import (
    ReservationError,
    availability,
    create_reservation,
    list_reservations,
    transition_reservation,
)

APP_DIR = Path(__file__).resolve().parents[1]


def create_app(test_config: dict | None = None) -> Flask:
    app = Flask(
        __name__,
        template_folder=str(APP_DIR / "views"),
        static_folder=str(APP_DIR / "static"),
    )
    app.config.update(
        SECRET_KEY=os.getenv("SECRET_KEY", "dev-only-change-me"),
        SESSION_COOKIE_HTTPONLY=True,
        SESSION_COOKIE_SAMESITE="Lax",
        SESSION_COOKIE_SECURE=os.getenv("COOKIE_SECURE", "0") == "1",
        JSON_SORT_KEYS=False,
    )
    if test_config:
        app.config.update(test_config)

    logging.basicConfig(level=os.getenv("LOG_LEVEL", "INFO"))
    init_database(seed_demo=os.getenv("SEED_DEMO_USERS", "1") != "0")

    def current_user():
        user_id = session.get("user_id")
        return get_user_by_id(user_id) if user_id else None

    def require_user():
        user = current_user()
        if not user:
            return None, (jsonify({"success": False, "message": "Authentication required."}), 401)
        return user, None

    def establish_session(user: dict, remember: bool = False):
        session.clear()
        session["user_id"] = user["id"]
        session["email"] = user["email"]
        session["full_name"] = user["full_name"]
        session["role"] = user["role"]
        session.permanent = bool(remember)

    @app.get("/")
    def home():
        return render_template("index.html")

    @app.get("/login")
    def login_page():
        return render_template("login.html")

    @app.get("/signup")
    def signup_page():
        return render_template("signup.html")

    @app.get("/reservations")
    def reservations_page():
        return render_template("reservations.html")

    @app.get("/restaurant-listing")
    def restaurant_listing_page():
        return render_template("restaurant-listing.html")

    @app.get("/restaurant-detail")
    def restaurant_detail_page():
        return render_template("restaurant-detail.html")

    @app.get("/booking-form")
    def booking_form_page():
        return render_template("booking-form.html")

    @app.post("/api/signup")
    def signup():
        data = request.get_json(silent=True) or {}
        success, message, user_id = register_user(
            data.get("full_name"), data.get("email"), data.get("phone"),
            data.get("country_code", "+961"), data.get("password"),
        )
        if not success:
            return jsonify({"success": False, "message": message}), 400
        user = get_user_by_id(user_id)
        establish_session(user)
        app.logger.info("signup user_id=%s", user_id)
        return jsonify({"success": True, "message": message, "user": user}), 201

    @app.post("/api/login")
    def login():
        data = request.get_json(silent=True) or {}
        success, message, user = login_user(data.get("email"), data.get("password"))
        if not success:
            return jsonify({"success": False, "message": message}), 401
        establish_session(user, bool(data.get("remember")))
        app.logger.info("login user_id=%s role=%s", user["id"], user["role"])
        return jsonify({"success": True, "message": message, "user": user})

    @app.post("/api/demo-login")
    def demo_login():
        data = request.get_json(silent=True) or {}
        role = str(data.get("role") or "DINER").upper()
        demo = DEMO_STAFF if role == "STAFF" else DEMO_DINER if role == "DINER" else None
        if not demo:
            return jsonify({"success": False, "message": "Demo role must be DINER or STAFF."}), 400
        user = get_user_by_email(demo["email"])
        if not user:
            return jsonify({"success": False, "message": "Demo identity is unavailable."}), 503
        establish_session(user)
        app.logger.info("demo_login role=%s user_id=%s", role, user["id"])
        return jsonify({"success": True, "user": user})

    @app.post("/api/logout")
    def logout():
        session.clear()
        return jsonify({"success": True, "message": "Logged out successfully"})

    @app.get("/api/user")
    def get_current_user():
        user, error = require_user()
        if error:
            return error
        return jsonify({"success": True, "user": user})

    @app.get("/api/check-auth")
    def check_auth():
        user = current_user()
        return jsonify({"authenticated": bool(user), "user": user})

    @app.get("/api/reservations")
    def get_reservations():
        user, error = require_user()
        if error:
            return error
        return jsonify({"success": True, "reservations": list_reservations(user)})

    @app.post("/api/reservations")
    def post_reservation():
        user, error = require_user()
        if error:
            return error
        try:
            reservation = create_reservation(user, request.get_json(silent=True) or {})
        except ReservationError as exc:
            return jsonify({"success": False, "message": exc.message}), exc.status_code
        app.logger.info(
            "reservation_created id=%s user_id=%s restaurant_id=%s",
            reservation["id"], user["id"], reservation["restaurantId"],
        )
        return jsonify({"success": True, "reservation": reservation}), 201

    @app.get("/api/reservations/availability")
    def reservation_availability():
        try:
            result = availability(
                request.args.get("restaurant_id"),
                request.args.get("date"),
                request.args.get("time"),
            )
        except ReservationError as exc:
            return jsonify({"success": False, "message": exc.message}), exc.status_code
        return jsonify({"success": True, **result})

    @app.patch("/api/reservations/<int:reservation_id>/status")
    def patch_reservation_status(reservation_id: int):
        user, error = require_user()
        if error:
            return error
        data = request.get_json(silent=True) or {}
        try:
            reservation = transition_reservation(user, reservation_id, data.get("status"))
        except ReservationError as exc:
            return jsonify({"success": False, "message": exc.message}), exc.status_code
        app.logger.info(
            "reservation_transition id=%s actor=%s role=%s status=%s",
            reservation_id, user["id"], user["role"], reservation["status"],
        )
        return jsonify({"success": True, "reservation": reservation})

    @app.get("/api/ml/predict")
    def ml_predict():
        try:
            temp = float(request.args.get("temp", 25))
            wind = float(request.args.get("wind", 10))
            rain_raw = str(request.args.get("rain", "false")).lower()
            if rain_raw not in {"true", "false"}:
                raise PredictionInputError("Rain must be true or false.")
            result = predict_today(temp, rain_raw == "true", wind)
        except (ValueError, PredictionInputError) as exc:
            return jsonify({"success": False, "message": str(exc), "advisory": True}), 400
        status = 200 if result.get("success") else 503
        return jsonify(result), status

    @app.get("/api/health")
    def health_check():
        db_ok, db_error = database_health()
        ml_ok, ml_error = model_health()
        release = (
            os.getenv("RELEASE_SHA")
            or os.getenv("RAILWAY_GIT_COMMIT_SHA")
            or os.getenv("RENDER_GIT_COMMIT")
            or "local"
        )
        secret_ok = app.config.get("SECRET_KEY") != "dev-only-change-me"
        healthy = db_ok and ml_ok and secret_ok
        payload = {
            "status": "healthy" if healthy else "degraded",
            "release": release,
            "checks": {
                "database": {"ok": db_ok, "error": db_error},
                "ml_model": {"ok": ml_ok, "error": ml_error},
                "configuration": {
                    "ok": secret_ok,
                    "error": None if secret_ok else "SECRET_KEY is still the development default.",
                },
            },
        }
        return jsonify(payload), 200 if healthy else 503

    @app.errorhandler(404)
    def not_found(error):
        if request.path.startswith("/api/"):
            return jsonify({"success": False, "message": "API route not found."}), 404
        return error

    @app.errorhandler(500)
    def server_error(error):
        app.logger.exception("unhandled_server_error")
        if request.path.startswith("/api/"):
            return jsonify({"success": False, "message": "Unexpected server error."}), 500
        return error

    return app


app = create_app()


if __name__ == "__main__":
    port = int(os.getenv("PORT", "5000"))
    app.run(host="0.0.0.0", port=port, debug=os.getenv("FLASK_DEBUG", "0") == "1")
