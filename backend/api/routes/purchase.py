"""Purchase routes."""
from fastapi import APIRouter, HTTPException
from api.models.purchase import PurchaseRequest
# from api.services.purchase_service import process_purchase
from db.connector import conn
from db.dao.order_dao import OrderDAO

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
