"""Purchase routes."""
from fastapi import APIRouter, HTTPException
from api.models.purchase import PurchaseRequest
from api.services.purchase_service import process_purchase

router = APIRouter()


@router.post("/purchase")
async def purchase(body: PurchaseRequest):
    if body.qty < 1:
        raise HTTPException(status_code=400, detail="qty must be >= 1")

    result = process_purchase(body.itemId, body.qty)
    if result is None:
        raise HTTPException(status_code=404, detail="item not found")

    return result
