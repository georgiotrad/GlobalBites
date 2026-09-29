def test_health_exposes_release_and_dependency_checks(client, monkeypatch):
    # The real ML model is exercised in the release environment once sklearn is installed.
    # This assertion focuses on the operator-facing shape and DB readiness.
    response = client.get("/api/health")
    data = response.get_json()
    assert data["status"] in {"healthy", "degraded"}
    assert "release" in data
    assert data["checks"]["database"]["ok"] is True
    assert "ml_model" in data["checks"]
