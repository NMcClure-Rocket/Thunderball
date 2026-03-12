"""
Integration tests for the Thunderball API.
Tests the full request/response cycle against the live ASGI app.
"""
import pytest
from fastapi.testclient import TestClient
from api.main import app


@pytest.fixture(scope="module")
def client():
    with TestClient(app) as c:
        yield c


def test_health_check_full_cycle(client):
    """Health endpoint returns 200 with correct payload."""
    response = client.get("/health")
    assert response.status_code == 200
    body = response.json()
    assert "status" in body
    assert body["status"] == "healthy"


def test_root_full_cycle(client):
    """Root endpoint returns 200 with an informational message."""
    response = client.get("/")
    assert response.status_code == 200
    body = response.json()
    assert "message" in body
    assert isinstance(body["message"], str)
    assert len(body["message"]) > 0


def test_all_endpoints_return_json(client):
    """Every public endpoint must return JSON content-type."""
    for path in ["/", "/health"]:
        response = client.get(path)
        assert "application/json" in response.headers["content-type"], (
            f"{path} did not return JSON"
        )


def test_openapi_schema_has_both_routes(client):
    """OpenAPI schema must document all exposed routes."""
    schema = client.get("/openapi.json").json()
    paths = schema.get("paths", {})
    assert "/" in paths, "Root route missing from schema"
    assert "/health" in paths, "Health route missing from schema"


def test_cors_header_for_allowed_origin(client):
    """Allowed origin should receive CORS header."""
    response = client.get(
        "/health", headers={"Origin": "http://localhost:3000"}
    )
    assert response.status_code == 200
    assert "access-control-allow-origin" in response.headers
