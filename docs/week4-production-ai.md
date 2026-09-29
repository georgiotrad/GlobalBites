# Week 4 — Production AI / ML Evidence

## Runtime capability
The homepage calls `/api/ml/predict`, which loads the supplied `DecisionTreeRegressor` model and predicts outdoor booking demand from temperature, rain, wind, day and season.

## Trusted boundary
Product code bounds temperature (-30..60 C), wind (0..200 km/h), and rain (boolean). Day and season are derived by software, not supplied as arbitrary model context.

## AI/ML is not authority
The prediction may recommend outdoor preparation. It never accepts/rejects a reservation, never marks a table booked, never changes state, never decides role/ownership, and never writes reservation data.

## Safe failure
- bad input -> 400;
- missing/unloadable model -> safe unavailable response;
- model exception -> safe unavailable response;
- NaN/infinite/out-of-range output -> rejected;
- UI shows an unavailable advisory while deterministic reservations continue.

## Eval command
`python -m pytest -q tests/test_ml_eval.py`

The 8 cases cover low, medium, high, rain/context behavior, invalid temperature, invalid wind, invalid model output, and provider/model failure.
