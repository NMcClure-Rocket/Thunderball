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


# ===========================================================================
# GET / and GET /health
# ===========================================================================

def test_root_returns_200(client):
    assert client.get("/").status_code == 200


def test_root_message(client):
    assert client.get("/").json() == {"message": "Thunderball API is running"}


def test_health_returns_200(client):
    assert client.get("/health").status_code == 200


def test_health_returns_healthy(client):
    assert client.get("/health").json() == {"status": "healthy"}


# ===========================================================================
# GET /pulse
# ===========================================================================

def test_pulse_returns_200(client):
    assert client.get("/pulse").status_code == 200


def test_pulse_payload_shape(client):
    body = client.get("/pulse").json()
    assert body["status"] == "ok"
    assert isinstance(body["timestamp"], int)
    assert body["timestamp"] > 0


# ===========================================================================
# GET /inventory
# ===========================================================================

def test_get_inventory_returns_200(client):
    assert client.get("/inventory").status_code == 200


def test_get_inventory_returns_items_list(client):
    body = client.get("/inventory").json()
    assert "items" in body
    assert isinstance(body["items"], list)
    assert len(body["items"]) > 0


def test_get_inventory_items_have_expected_fields(client):
    items = client.get("/inventory").json()["items"]
    for item in items:
        assert "id" in item
        assert "name" in item
        assert "price" in item
        assert "image" in item


def test_get_inventory_prices_are_positive(client):
    items = client.get("/inventory").json()["items"]
    for item in items:
        assert item["price"] > 0


# ===========================================================================
# GET /inventory/{item_id}
# ===========================================================================

def test_get_inventory_item_returns_200(client):
    assert client.get("/inventory/1").status_code == 200


def test_get_inventory_item_returns_correct_item(client):
    body = client.get("/inventory/1").json()
    assert body["id"] == 1
    assert "name" in body
    assert "price" in body
    assert "image" in body


def test_get_inventory_item_not_found_returns_404(client):
    assert client.get("/inventory/9999").status_code == 404


def test_get_inventory_item_not_found_detail(client):
    body = client.get("/inventory/9999").json()
    assert "detail" in body
    assert body["detail"] == "item not found"


def test_get_inventory_item_all_seeded_ids_exist(client):
    for item_id in [1, 2, 3]:
        assert client.get(f"/inventory/{item_id}").status_code == 200


# ===========================================================================
# POST /logon
# ===========================================================================

def test_logon_returns_200(client):
    assert client.post("/logon", json={"user": "alice", "pass": "secret"}).status_code == 200


def test_logon_echoes_user(client):
    body = client.post("/logon", json={"user": "alice", "pass": "secret"}).json()
    assert body["status"] == "ok"
    assert body["user"] == "alice"


def test_logon_missing_fields_returns_422(client):
    assert client.post("/logon", json={}).status_code == 422


def test_logon_missing_password_returns_422(client):
    assert client.post("/logon", json={"user": "alice"}).status_code == 422


def test_logon_missing_user_returns_422(client):
    assert client.post("/logon", json={"pass": "secret"}).status_code == 422


# ===========================================================================
# POST /purchase
# ===========================================================================

def test_purchase_returns_200(client):
    assert client.post("/purchase", json={"itemId": 1, "qty": 2}).status_code == 200


def test_purchase_payload_shape(client):
    body = client.post("/purchase", json={"itemId": 1, "qty": 2}).json()
    assert body["status"] == "ok"
    assert "orderId" in body
    assert body["item"] is not None
    assert body["qty"] == 2
    assert "total" in body


def test_purchase_total_is_price_times_qty(client):
    inventory = client.get("/inventory").json()["items"]
    item = next(i for i in inventory if i["id"] == 1)
    body = client.post("/purchase", json={"itemId": 1, "qty": 3}).json()
    assert abs(body["total"] - item["price"] * 3) < 0.001


def test_purchase_qty_zero_returns_400(client):
    assert client.post("/purchase", json={"itemId": 1, "qty": 0}).status_code == 400


def test_purchase_negative_qty_returns_400(client):
    assert client.post("/purchase", json={"itemId": 1, "qty": -5}).status_code == 400


def test_purchase_qty_error_detail(client):
    body = client.post("/purchase", json={"itemId": 1, "qty": 0}).json()
    assert body["detail"] == "qty must be >= 1"


def test_purchase_unknown_item_returns_404(client):
    assert client.post("/purchase", json={"itemId": 9999, "qty": 1}).status_code == 404


def test_purchase_unknown_item_detail(client):
    body = client.post("/purchase", json={"itemId": 9999, "qty": 1}).json()
    assert body["detail"] == "item not found"


def test_purchase_missing_fields_returns_422(client):
    assert client.post("/purchase", json={"itemId": 1}).status_code == 422


# ===========================================================================
# Cross-cutting concerns
# ===========================================================================

def test_all_get_endpoints_return_json(client):
    for path in ["/", "/health", "/pulse", "/inventory", "/inventory/1"]:
        response = client.get(path)
        assert "application/json" in response.headers["content-type"], (
            f"{path} did not return JSON"
        )


def test_cors_header_present_for_allowed_origin(client):
    response = client.get("/pulse", headers={"Origin": "http://localhost:3000"})
    assert response.status_code == 200
    assert "access-control-allow-origin" in response.headers


def test_openapi_schema_lists_server_routes(client):
    paths = client.get("/openapi.json").json().get("paths", {})
    for route in ["/logon", "/inventory", "/inventory/{item_id}", "/pulse", "/purchase"]:
        assert route in paths, f"{route} missing from OpenAPI schema"
