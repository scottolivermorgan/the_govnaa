from app.api.health import health


def test_health_reports_configured_root() -> None:
    response = health()

    assert response["status"] == "ok"
    assert response["roots"][0]["id"] == "test-media"
