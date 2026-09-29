def test_signup_hashes_password_and_creates_diner_session(client):
    response = client.post(
        "/api/signup",
        json={
            "full_name": "Test User",
            "email": "test.user@example.com",
            "phone": "70111222",
            "country_code": "+961",
            "password": "secret123",
        },
    )
    assert response.status_code == 201
    assert response.get_json()["user"]["role"] == "DINER"

    current = client.get("/api/user")
    assert current.status_code == 200
    assert current.get_json()["user"]["email"] == "test.user@example.com"


def test_invalid_signup_is_rejected(client):
    response = client.post(
        "/api/signup",
        json={
            "full_name": "A",
            "email": "not-an-email",
            "phone": "",
            "password": "1",
        },
    )
    assert response.status_code == 400
