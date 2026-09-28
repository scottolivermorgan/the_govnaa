from app.api.health import health, index


def test_index_points_to_health_endpoint() -> None:
    response = index()

    assert response == {
        "name": "Data Governor",
        "status": "running",
        "health": "/health",
    }


def test_health_reports_configured_root() -> None:
    response = health()

    assert response["status"] == "ok"
    assert response["roots"][0]["id"] == "test-media"
