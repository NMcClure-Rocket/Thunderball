"""Inventory routes."""
from fastapi import APIRouter, HTTPException
from api.services.inventory_service import get_all_items, get_item_by_id

router = APIRouter()


@router.get("/inventory")
async def get_inventory():
    return {"items": get_all_items()}


@router.get("/inventory/{item_id}")
async def get_inventory_item(item_id: int):
    item = get_item_by_id(item_id)
    if not item:
        raise HTTPException(status_code=404, detail="item not found")
    return item
