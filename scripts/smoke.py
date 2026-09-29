"""Live critical-path smoke test using only Python's standard library.

Usage: python scripts/smoke.py https://your-live-url
It creates one demo reservation, confirms it as staff, then cancels it so the
active slot is released while the audit row remains persisted.
"""
from __future__ import annotations

import json
import sys
from datetime import date, timedelta
from http.cookiejar import CookieJar
from urllib.error import HTTPError
from urllib.parse import urlencode
from urllib.request import HTTPCookieProcessor, Request, build_opener

BASE = (sys.argv[1] if len(sys.argv) > 1 else "http://127.0.0.1:5000").rstrip("/")
jar = CookieJar()
opener = build_opener(HTTPCookieProcessor(jar))


def call(path, method="GET", payload=None):
    data = json.dumps(payload).encode() if payload is not None else None
    req = Request(BASE + path, data=data, method=method)
    if data is not None:
        req.add_header("Content-Type", "application/json")
    try:
        with opener.open(req, timeout=30) as response:
            return response.status, json.loads(response.read().decode())
    except HTTPError as exc:
        body = json.loads(exc.read().decode())
        raise RuntimeError(f"{method} {path} -> {exc.code}: {body}") from exc


print("1/7 health")
status, health = call("/api/health")
assert status == 200 and health["status"] == "healthy", health
print("   release:", health["release"])

print("2/7 ML advisory")
status, ml = call("/api/ml/predict?temp=25&rain=false&wind=10")
assert status == 200 and ml["success"] and ml["advisory"]

print("3/7 demo diner login")
call("/api/demo-login", "POST", {"role": "DINER"})

future = (date.today() + timedelta(days=30)).isoformat()
slot = urlencode({"restaurant_id": 1, "date": future, "time": "20:30"})
_, availability = call("/api/reservations/availability?" + slot)
if not availability["available"]:
    raise RuntimeError("No table available for smoke-test slot")
table = availability["available"][0]
seating = "outdoor" if table.startswith("O") else "indoor"
capacity = 2 if table in {"T1", "T4", "O1"} else 4

print("4/7 create persisted reservation")
_, created = call("/api/reservations", "POST", {
    "restaurant_id": 1,
    "date": future,
    "time": "20:30",
    "guests": min(2, capacity),
    "table": table,
    "seating_type": seating,
})
reservation_id = created["reservation"]["id"]
assert created["reservation"]["status"] == "PENDING"

print("5/7 staff login and confirm")
call("/api/demo-login", "POST", {"role": "STAFF"})
_, confirmed = call(f"/api/reservations/{reservation_id}/status", "PATCH", {"status": "CONFIRMED"})
assert confirmed["reservation"]["status"] == "CONFIRMED"

print("6/7 persisted state visible")
_, all_rows = call("/api/reservations")
assert any(row["id"] == reservation_id and row["status"] == "CONFIRMED" for row in all_rows["reservations"])

print("7/7 cleanup active slot via valid staff transition")
_, cancelled = call(f"/api/reservations/{reservation_id}/status", "PATCH", {"status": "CANCELLED"})
assert cancelled["reservation"]["status"] == "CANCELLED"
print("SMOKE: PASS reservation", reservation_id)
