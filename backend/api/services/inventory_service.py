"""
Inventory service – business logic for inventory operations.

The hardcoded data here is a placeholder until the Db2 adapter is ready.
"""

# ── Placeholder inventory data ─────────────────────────────────
_inventory = [
    {"id": 1, "name": "Duck Spell A", "price": 9.99,  "image": "duck-a.png"},
    {"id": 2, "name": "Duck Spell B", "price": 12.50, "image": "duck-b.png"},
    {"id": 3, "name": "Fire Spell",   "price": 5.00,  "image": "fire.png"},
]


def get_all_items() -> list[dict]:
    """Return every item in the catalogue."""
    return list(_inventory)


def get_item_by_id(item_id: int) -> dict | None:
    """Look up a single item.  Returns None when not found."""
    return next((i for i in _inventory if i["id"] == item_id), None)
