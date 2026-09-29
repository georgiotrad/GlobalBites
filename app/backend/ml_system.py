"""Bounded ML advisory used by the GlobalBites homepage.

The model estimates outdoor booking demand. It is advisory only and never
controls table availability, authorization, reservation status, or persistence.
"""

from __future__ import annotations

import math
import os
import pickle
from datetime import datetime
from pathlib import Path

MODEL_PATH = Path(os.getenv(
    "GLOBALBITES_ML_MODEL_PATH",
    str(Path(__file__).resolve().parent / "outdoor_booking_model.pkl"),
))


class PredictionInputError(ValueError):
    pass


def load_model():
    if os.getenv("GLOBALBITES_ML_FORCE_FAILURE") == "1":
        raise RuntimeError("ML failure simulation is enabled.")
    with MODEL_PATH.open("rb") as file:
        return pickle.load(file)


def model_health() -> tuple[bool, str | None]:
    try:
        model = load_model()
        if not hasattr(model, "predict"):
            return False, "Loaded object does not provide predict()."
        return True, None
    except Exception as exc:
        return False, str(exc)


def _bounded_inputs(temperature, is_raining, wind_speed):
    try:
        temperature = float(temperature)
        wind_speed = float(wind_speed)
    except (TypeError, ValueError):
        raise PredictionInputError("Temperature and wind speed must be numeric.")

    if not -30 <= temperature <= 60:
        raise PredictionInputError("Temperature must be between -30 and 60 °C.")
    if not 0 <= wind_speed <= 200:
        raise PredictionInputError("Wind speed must be between 0 and 200 km/h.")
    if not isinstance(is_raining, bool):
        raise PredictionInputError("Rain must be true or false.")
    return temperature, is_raining, wind_speed


def predict_today(temperature=25, is_raining=False, wind_speed=10, *, model_loader=load_model, now=None):
    temperature, is_raining, wind_speed = _bounded_inputs(
        temperature, is_raining, wind_speed
    )

    try:
        model = model_loader()
    except Exception as exc:
        return {
            "success": False,
            "message": "Outdoor demand prediction is temporarily unavailable.",
            "advisory": True,
        }

    if not hasattr(model, "predict"):
        return {
            "success": False,
            "message": "Outdoor demand prediction is temporarily unavailable.",
            "advisory": True,
        }

    current = now or datetime.now()
    day_name = current.strftime("%A")
    day_number = {
        "Monday": 1, "Tuesday": 2, "Wednesday": 3, "Thursday": 4,
        "Friday": 5, "Saturday": 6, "Sunday": 7,
    }[day_name]

    month = current.month
    if month in (12, 1, 2):
        season, season_number = "winter", 1
    elif month in (3, 4, 5):
        season, season_number = "spring", 2
    elif month in (6, 7, 8):
        season, season_number = "summer", 3
    else:
        season, season_number = "fall", 4

    try:
        result = model.predict([[temperature, 1 if is_raining else 0, wind_speed, day_number, season_number]])
        predicted_bookings = float(result[0])
    except Exception as exc:
        return {
            "success": False,
            "message": "Outdoor demand prediction is temporarily unavailable.",
            "advisory": True,
        }

    if not math.isfinite(predicted_bookings) or predicted_bookings < 0 or predicted_bookings > 10000:
        return {
            "success": False,
            "message": "The ML model returned an invalid prediction.",
            "advisory": True,
        }

    predicted_bookings = round(predicted_bookings, 1)
    if predicted_bookings < 3:
        recommendation, status = "No outdoor cleaning needed", "low"
    elif predicted_bookings < 8:
        recommendation, status = "Light outdoor cleaning recommended", "medium"
    else:
        recommendation, status = "Prepare outdoor seating - higher demand expected", "high"

    return {
        "success": True,
        "bookings": predicted_bookings,
        "recommendation": recommendation,
        "status": status,
        "advisory": True,
        "authority": "Reservation availability and lifecycle remain deterministic software rules.",
        "weather": {
            "temp": temperature,
            "rain": is_raining,
            "wind": wind_speed,
            "day": day_name,
            "season": season,
        },
    }
