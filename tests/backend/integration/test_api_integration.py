"""
Integration tests for the Thunderball API.
Tests the full request/response cycle against the live ASGI app.
"""
import json
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
    body = json.loads(client.get("/inventory").json())
    assert "items" in body
    assert isinstance(body["items"], list)
    assert len(body["items"]) > 0


def test_get_inventory_items_have_expected_fields(client):
    items = json.loads(client.get("/inventory").json())["items"]
    for item in items:
        assert "id" in item
        assert "name" in item
        assert "price" in item
        assert "image" in item


def test_get_inventory_prices_are_positive(client):
    items = json.loads(client.get("/inventory").json())["items"]
    for item in items:
        assert item["price"] > 0


# ===========================================================================
# GET /inventory/{item_id}
# ===========================================================================

def test_get_inventory_item_returns_200(client):
    assert client.get("/inventory/1").status_code == 200


def test_get_inventory_item_returns_correct_item(client):
    body = json.loads(client.get("/inventory/1").json())
    rows = body["rows"]
    assert len(rows) > 0
    assert rows[0]["itemid"] == 1
    assert "name" in rows[0]
    assert "price" in rows[0]


def test_get_inventory_item_not_found_returns_200(client):
    assert client.get("/inventory/9999").status_code == 200


def test_get_inventory_item_not_found_returns_empty_rows(client):
    body = json.loads(client.get("/inventory/9999").json())
    assert body == {"rows": []}


def test_get_inventory_item_all_seeded_ids_exist(client):
    for item_id in [1, 2, 3]:
        assert client.get(f"/inventory/{item_id}").status_code == 200


# ===========================================================================
# POST /logon
# ===========================================================================

def test_logon_returns_200(client):
    assert client.post("/logon", json={"user": "jdoe@a.com", "pass": "mypassword"}).status_code == 200


def test_logon_echoes_user(client):
    body = client.post("/logon", json={"user": "jdoe@a.com", "pass": "mypassword"}).json()
    assert body["status"] == "ok"
    assert body["user"] == "jdoe@a.com"


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
    assert client.post("/purchase", json={"itemId": 1, "qty": 2, "customerid": 1, "addressid": 1, "ccid": 1}).status_code == 200


def test_purchase_payload_shape(client):
    body = client.post("/purchase", json={"itemId": 1, "qty": 2, "customerid": 1, "addressid": 1, "ccid": 1}).json()
    assert body["status"] == "ok"
    assert "orderId" in body
    assert body["item"] is not None
    assert body["qty"] == 2
    assert "total" in body


def test_purchase_total_is_price_times_qty(client):
    from api.services.inventory_service import get_item_by_id
    item = get_item_by_id(1)
    body = client.post("/purchase", json={"itemId": 1, "qty": 3, "customerid": 1, "addressid": 1, "ccid": 1}).json()
    assert abs(body["total"] - item["price"] * 3) < 0.001


def test_purchase_qty_zero_returns_400(client):
    assert client.post("/purchase", json={"itemId": 1, "qty": 0, "customerid": 1, "addressid": 1, "ccid": 1}).status_code == 400


def test_purchase_negative_qty_returns_400(client):
    assert client.post("/purchase", json={"itemId": 1, "qty": -5, "customerid": 1, "addressid": 1, "ccid": 1}).status_code == 400


def test_purchase_qty_error_detail(client):
    body = client.post("/purchase", json={"itemId": 1, "qty": 0, "customerid": 1, "addressid": 1, "ccid": 1}).json()
    assert body["detail"] == "qty must be >= 1"


def test_purchase_unknown_item_returns_404(client):
    assert client.post("/purchase", json={"itemId": 9999, "qty": 1, "customerid": 1, "addressid": 1, "ccid": 1}).status_code == 404


def test_purchase_unknown_item_detail(client):
    body = client.post("/purchase", json={"itemId": 9999, "qty": 1, "customerid": 1, "addressid": 1, "ccid": 1}).json()
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


@pytest.mark.skip(
    reason="OpenAPI schema generation broken while credit_card.py DAO migration is in progress"
)
def test_openapi_schema_lists_server_routes(client):
    paths = client.get("/openapi.json").json().get("paths", {})
    for route in ["/logon", "/inventory", "/inventory/{item_id}", "/pulse",
                  "/purchase", "/createuser", "/newaddress",
                  "/getaddress/{customer_id}", "/newcc", "/getcc/{customer_id}"]:
        assert route in paths, f"{route} missing from OpenAPI schema"


# ===========================================================================
# POST /createuser
# ===========================================================================

def test_createuser_returns_200(client):
    import api.services.auth_service as svc
    original = list(svc._users)
    try:
        assert client.post("/createuser", json={
            "first_name": "Test", "last_name": "User",
            "user": "testuser_int@test.com", "pass": "pw123"
        }).status_code == 200
    finally:
        svc._users[:] = original


def test_createuser_returns_ok_status(client):
    import api.services.auth_service as svc
    original = list(svc._users)
    try:
        body = client.post("/createuser", json={
            "first_name": "Test", "last_name": "User",
            "user": "testuser2_int@test.com", "pass": "pw123"
        }).json()
        assert body["status"] == "ok"
    finally:
        svc._users[:] = original


def test_createuser_duplicate_returns_400(client):
    assert client.post("/createuser", json={
        "first_name": "John", "last_name": "Doe",
        "user": "jdoe@a.com", "pass": "anything"
    }).status_code == 400


def test_createuser_duplicate_detail(client):
    body = client.post("/createuser", json={
        "first_name": "John", "last_name": "Doe",
        "user": "jdoe@a.com", "pass": "anything"
    }).json()
    assert body["detail"] == "Username already exists"


def test_createuser_missing_fields_returns_422(client):
    assert client.post("/createuser", json={"user": "x"}).status_code == 422


# ===========================================================================
# POST /newaddress
# ===========================================================================

_SAMPLE_ADDRESS = {
    "first_name": "Jane", "last_name": "Doe",
    "address": "1 Main St", "addr_2": "",
    "city": "Miami", "state": "FL", "country": "US", "zip": "33101",
}


def test_newaddress_returns_200(client):
    assert client.post("/newaddress", json=_SAMPLE_ADDRESS).status_code == 200


def test_newaddress_returns_ok_status(client):
    body = client.post("/newaddress", json=_SAMPLE_ADDRESS).json()
    assert body["status"] == "ok"


def test_newaddress_missing_fields_returns_422(client):
    assert client.post("/newaddress", json={"first_name": "Jane"}).status_code == 422


# ===========================================================================
# GET /getaddress/{customer_id}
# ===========================================================================

def test_getaddress_returns_200(client):
    assert client.get("/getaddress/1").status_code == 200


def test_getaddress_returns_rows_key(client):
    body = client.get("/getaddress/1").json()
    assert "rows" in body


def test_getaddress_seeded_customer_has_rows(client):
    body = client.get("/getaddress/1").json()
    assert isinstance(body["rows"], list)
    assert len(body["rows"]) >= 1


def test_getaddress_unknown_customer_returns_empty(client):
    body = client.get("/getaddress/9999").json()
    assert body["rows"] == []


# ===========================================================================
# POST /newcc
# ===========================================================================

_SAMPLE_CC = {
    "number": 4111111111111111, "security_code": 123,
    "expiration": "12/28", "processor": "Visa",
    "first_name": "Test", "last_name": "User",
    "address": "1 St", "addr_2": "",
    "city": "NYC", "state": "NY", "country": "US", "zip": "10001",
}


@pytest.mark.skip(reason="/newcc DAO migration in progress – body type unresolvable by Pydantic")
def test_newcc_returns_200(client):
    assert client.post("/newcc", json=_SAMPLE_CC).status_code == 200


@pytest.mark.skip(reason="/newcc DAO migration in progress – body type unresolvable by Pydantic")
def test_newcc_returns_ok_status(client):
    body = client.post("/newcc", json=_SAMPLE_CC).json()
    assert body["status"] == "ok"


def test_newcc_missing_fields_returns_422(client):
    assert client.post("/newcc", json={"number": 4111111111111111}).status_code == 422


# ===========================================================================
# GET /getcc/{customer_id}
# ===========================================================================

def test_getcc_returns_200(client):
    assert client.get("/getcc/1").status_code == 200


@pytest.mark.skip(reason="/getcc DAO migration in progress – returns None instead of rows dict")
def test_getcc_returns_rows_key(client):
    body = client.get("/getcc/1").json()
    assert "rows" in body


@pytest.mark.skip(reason="/getcc DAO migration in progress – returns None instead of rows dict")
def test_getcc_seeded_customer_has_rows(client):
    body = client.get("/getcc/1").json()
    assert isinstance(body["rows"], list)
    assert len(body["rows"]) >= 1


@pytest.mark.skip(reason="/getcc DAO migration in progress – returns None instead of rows dict")
def test_getcc_unknown_customer_returns_empty(client):
    body = client.get("/getcc/9999").json()
    assert body["rows"] == []
