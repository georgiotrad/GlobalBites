from datetime import date, timedelta


def demo_login(client, role):
    response = client.post("/api/demo-login", json={"role": role})
    assert response.status_code == 200
    return response.get_json()["user"]


def create_valid_reservation(client, table="T2"):
    future = (date.today() + timedelta(days=30)).isoformat()
    response = client.post(
        "/api/reservations",
        json={
            "restaurant_id": 1,
            "date": future,
            "time": "19:00",
            "guests": 2,
            "table": table,
            "seating_type": "indoor",
        },
    )
    return response


def test_diner_can_create_and_read_persisted_reservation(client):
    demo_login(client, "DINER")
    created = create_valid_reservation(client)
    assert created.status_code == 201
    reservation = created.get_json()["reservation"]
    assert reservation["status"] == "PENDING"
    assert reservation["restaurantName"] == "Swiss Butter"

    listed = client.get("/api/reservations")
    assert listed.status_code == 200
    ids = [item["id"] for item in listed.get_json()["reservations"]]
    assert reservation["id"] in ids


def test_duplicate_table_slot_is_rejected_without_mutating_original(client):
    demo_login(client, "DINER")
    first = create_valid_reservation(client)
    assert first.status_code == 201
    duplicate = create_valid_reservation(client)
    assert duplicate.status_code == 409
    assert "already reserved" in duplicate.get_json()["message"]

    listed = client.get("/api/reservations").get_json()["reservations"]
    assert len(listed) == 1
    assert listed[0]["status"] == "PENDING"


def test_staff_can_confirm_then_complete_valid_lifecycle(client):
    demo_login(client, "DINER")
    reservation_id = create_valid_reservation(client).get_json()["reservation"]["id"]

    demo_login(client, "STAFF")
    confirmed = client.patch(
        f"/api/reservations/{reservation_id}/status", json={"status": "CONFIRMED"}
    )
    assert confirmed.status_code == 200
    assert confirmed.get_json()["reservation"]["status"] == "CONFIRMED"

    completed = client.patch(
        f"/api/reservations/{reservation_id}/status", json={"status": "COMPLETED"}
    )
    assert completed.status_code == 200
    assert completed.get_json()["reservation"]["status"] == "COMPLETED"


def test_invalid_staff_transition_is_rejected_and_state_is_unchanged(client):
    demo_login(client, "DINER")
    reservation_id = create_valid_reservation(client).get_json()["reservation"]["id"]

    demo_login(client, "STAFF")
    invalid = client.patch(
        f"/api/reservations/{reservation_id}/status", json={"status": "COMPLETED"}
    )
    assert invalid.status_code == 400
    assert "Invalid transition" in invalid.get_json()["message"]

    reservations = client.get("/api/reservations").get_json()["reservations"]
    reservation = next(item for item in reservations if item["id"] == reservation_id)
    assert reservation["status"] == "PENDING"


def test_diner_cannot_perform_staff_confirmation(client):
    demo_login(client, "DINER")
    reservation_id = create_valid_reservation(client).get_json()["reservation"]["id"]
    denied = client.patch(
        f"/api/reservations/{reservation_id}/status", json={"status": "CONFIRMED"}
    )
    assert denied.status_code == 403

    reservation = client.get("/api/reservations").get_json()["reservations"][0]
    assert reservation["status"] == "PENDING"


def test_diner_can_cancel_own_active_reservation(client):
    demo_login(client, "DINER")
    reservation_id = create_valid_reservation(client).get_json()["reservation"]["id"]
    cancelled = client.patch(
        f"/api/reservations/{reservation_id}/status", json={"status": "CANCELLED"}
    )
    assert cancelled.status_code == 200
    assert cancelled.get_json()["reservation"]["status"] == "CANCELLED"


def test_booking_requires_authentication(client):
    response = create_valid_reservation(client)
    assert response.status_code == 401


def test_backend_rejects_table_capacity_violation(client):
    demo_login(client, "DINER")
    future = (date.today() + timedelta(days=30)).isoformat()
    response = client.post(
        "/api/reservations",
        json={
            "restaurant_id": 1,
            "date": future,
            "time": "19:00",
            "guests": 4,
            "table": "T1",
            "seating_type": "indoor",
        },
    )
    assert response.status_code == 400
    assert "at most 2 guests" in response.get_json()["message"]
