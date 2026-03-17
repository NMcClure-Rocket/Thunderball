"""Inventory routes."""
from fastapi import APIRouter, HTTPException
from api.services.inventory_service import get_all_items, get_item_by_id, get_all_items_by_id
from api.utils.json_utils import baseprice_json, inventory_json
from db.connector import conn
from db.dao.base_price_dao import BasePriceDAO

router = APIRouter()


@router.get("/inventory")
async def get_inventory():
    dao = BasePriceDAO(conn)
    rows = dao.get_all_records()
    items = baseprice_json(rows)
    return items


@router.get("/inventory/{item_id}")
async def get_inventory_item(item_id: int):
    item = get_all_items_by_id(item_id)
    if not item:
        raise HTTPException(status_code=404, detail="item not found")
    return item
