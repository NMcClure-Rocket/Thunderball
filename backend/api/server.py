"""
API route definitions – all endpoints live here
"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
import time

router = APIRouter()

# ── Base-price table (inventory data) ──────────────────────────
inventory = [
    {"id": 1, "name": "Duck Spell A", "price": 9.99,  "image": "duck-a.png"},
    {"id": 2, "name": "Duck Spell B", "price": 12.50, "image": "duck-b.png"},
    {"id": 3, "name": "Fire Spell",   "price": 5.00,  "image": "fire.png"},
]

# ── Request models ──────────────────────────────────────────────
class LogonRequest(BaseModel):
    model_config = {"populate_by_name": True}
    user: str
    pass_: str = Field(alias="pass")

class PurchaseRequest(BaseModel):
    itemId: int
    qty: int

# POST /logon – no authentication, just echoes the user back
@router.post("/logon")
async def logon(body: LogonRequest):
    return {"status": "ok", "user": body.user}

# GET /inventory – return all items from the base-price table
@router.get("/inventory")
async def get_inventory():
    return {"items": inventory}

# GET /inventory/{item_id} – lookup a single item by its unique ID
@router.get("/inventory/{item_id}")
async def get_inventory_item(item_id: int):
    item = next((i for i in inventory if i["id"] == item_id), None)
    if not item:
        raise HTTPException(status_code=404, detail="item not found")
    return item

# GET /pulse – health check / heartbeat
@router.get("/pulse")
async def pulse():
    return {"status": "ok", "timestamp": int(time.time() * 1000)}

# POST /purchase – process a purchase
@router.post("/purchase")
async def purchase(body: PurchaseRequest):
    if body.qty < 1:
        raise HTTPException(status_code=400, detail="qty must be >= 1")

    item = next((i for i in inventory if i["id"] == body.itemId), None)
    if not item:
        raise HTTPException(status_code=404, detail="item not found")

    total = item["price"] * body.qty
    return {
        "status": "ok",
        "orderId": int(time.time() * 1000),
        "item": item["name"],
        "qty": body.qty,
        "total": total,
    }
