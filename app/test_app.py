import pytest
from app import app

@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client

def test_index(client):
    """Test the root endpoint returns expected JSON and correct version"""
    rv = client.get("/")
    assert rv.status_code == 200
    json_data = rv.get_json()
    assert json_data["service"] == "checkout-api"
    assert json_data["version"] == "v2.4"
    assert json_data["message"] == "Release Readiness Demo"

def test_health_with_required_config(client, monkeypatch):
    monkeypatch.setenv("DATABASE_URL", "postgresql://example.invalid/checkout")
    monkeypatch.setenv("REDIS_URL", "redis://example.invalid:6379/0")
    rv = client.get("/health")
    assert rv.status_code == 200
    json_data = rv.get_json()
    assert json_data["status"] == "ready"
    assert json_data["checks"] == {"database": "configured", "redis": "configured"}


@pytest.mark.parametrize("missing", ["DATABASE_URL", "REDIS_URL"])
def test_health_rejects_missing_config(client, monkeypatch, missing):
    monkeypatch.setenv("DATABASE_URL", "postgresql://example.invalid/checkout")
    monkeypatch.setenv("REDIS_URL", "redis://example.invalid:6379/0")
    monkeypatch.delenv(missing)
    rv = client.get("/health")
    assert rv.status_code == 503
    assert rv.get_json()["status"] == "not_ready"
