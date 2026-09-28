from app.api.ui import dashboard


def test_dashboard_renders_main_controls() -> None:
    html = dashboard()

    assert "Data Governor" in html
    assert "Scan Test Media" in html
    assert "Generate Proposals" in html
    assert 'request("/scans")' in html
