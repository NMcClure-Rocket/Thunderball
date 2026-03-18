"""
Purchase service – business logic for processing purchases.
"""
import time
from api.services.inventory_service import get_item_by_id


def process_purchase(item_id: int, qty: int) -> dict | None:
    """
    Validate and execute a purchase.

    Returns the order dict on success, or None if the item doesn't exist.
    """
    item = get_item_by_id(item_id)
    if item is None:
        return None

    total = item["price"] * qty
    return {
        "status": "ok",
        "orderId": int(time.time() * 1000),
        "item": item["name"],
        "qty": qty,
        "total": total,
    }
