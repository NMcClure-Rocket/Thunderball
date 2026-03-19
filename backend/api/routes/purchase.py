"""Purchase routes."""
from fastapi import APIRouter, HTTPException
from api.models.purchase import PurchaseRequest
# from api.services.purchase_service import process_purchase
from db.connector import conn
from db.dao.order_dao import OrderDAO
from api.utils.json_utils import order_history_json

router = APIRouter()


@router.post("/purchase")
async def purchase(body: dict[str, list[PurchaseRequest]]):
    # if body.qty < 1:
    #     raise HTTPException(status_code=400, detail="qty must be >= 1")

    # result = process_purchase(body.itemId, body.qty)
    # if result is None:
    #     raise HTTPException(status_code=404, detail="item not found")

    # return result
    orders = body["orders"]
    success = False
    for o in orders:
        dao = OrderDAO(conn)
        success = dao.insert_order(o)
        if not success:
            break

    if success:
        return {"status": "ok"}
    else:
        return {"status": "error"}

@router.get("/orders/{customerid}")
async def get_order_history(customerid: int):
    dao = OrderDAO(conn)
    rows = dao.get_history(customerid)
    items = order_history_json(rows)
    return items