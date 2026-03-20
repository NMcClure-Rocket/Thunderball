"""Purchase routes."""
from typing import Any
from fastapi import APIRouter
from api.utils.json_utils import order_history_json
from db.connector import conn
from db.dao.order_dao import OrderDAO

# from api.models.purchase import PurchaseRequest
# from api.services.purchase_service import process_purchase

router = APIRouter()


@router.post("/purchase")
async def purchase(body: dict[str, list[dict[str, Any]]]):
    """Submit one or more purchase orders."""
    orders = body["orders"]
    success = False
    for o in orders:
        dao = OrderDAO(conn)
        success = dao.insert_order(o)
        if not success:
            break

    if success:
        return {"status": "ok"}
    return {"status": "error"}


@router.get("/orders/{customerid}")
async def get_order_history(customerid: int):
    """Return order history for a customer."""
    dao = OrderDAO(conn)
    rows = dao.get_history(customerid)
    items = order_history_json(rows)
    return items
