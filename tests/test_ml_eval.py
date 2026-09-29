from datetime import datetime

import pytest

from app.backend.ml_system import PredictionInputError, predict_today


class FakeModel:
    def __init__(self, value):
        self.value = value

    def predict(self, features):
        return [self.value]


class ExplodingModel:
    def predict(self, features):
        raise RuntimeError("provider/model failure")


def fixed_now():
    return datetime(2026, 7, 10, 12, 0, 0)


def test_clear_low_demand_case():
    result = predict_today(20, False, 5, model_loader=lambda: FakeModel(2.2), now=fixed_now())
    assert result["success"] is True
    assert result["status"] == "low"
    assert result["advisory"] is True


def test_medium_demand_case():
    result = predict_today(25, False, 10, model_loader=lambda: FakeModel(5.0), now=fixed_now())
    assert result["status"] == "medium"


def test_high_demand_case():
    result = predict_today(30, False, 5, model_loader=lambda: FakeModel(12.0), now=fixed_now())
    assert result["status"] == "high"


def test_rain_is_bounded_product_input():
    result = predict_today(22, True, 12, model_loader=lambda: FakeModel(4.0), now=fixed_now())
    assert result["weather"]["rain"] is True


def test_out_of_range_temperature_is_rejected():
    with pytest.raises(PredictionInputError):
        predict_today(100, False, 10, model_loader=lambda: FakeModel(4.0), now=fixed_now())


def test_out_of_range_wind_is_rejected():
    with pytest.raises(PredictionInputError):
        predict_today(25, False, 999, model_loader=lambda: FakeModel(4.0), now=fixed_now())


def test_invalid_model_output_is_rejected_safely():
    result = predict_today(25, False, 10, model_loader=lambda: FakeModel(float("nan")), now=fixed_now())
    assert result["success"] is False
    assert "invalid prediction" in result["message"].lower()


def test_model_failure_is_safe_and_does_not_claim_authority():
    result = predict_today(25, False, 10, model_loader=lambda: ExplodingModel(), now=fixed_now())
    assert result["success"] is False
    assert result["advisory"] is True
