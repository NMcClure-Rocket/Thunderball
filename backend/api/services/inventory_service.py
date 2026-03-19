"""
Inventory service – business logic for inventory operations.

The hardcoded data here is a placeholder until the Db2 adapter is ready.
"""

# ── Placeholder BasePrice table data ─────────────────────────────────
_baseprice = [
    # {"id": 1, "name": "Duck Spell", "price": 9.99, "image": "duck-a.png"},
    # {"id": 2, "name": "Other Spell", "price": 12.50, "image": "duck-b.png"},
    # {"id": 3, "name": "Fire Spell",   "price": 5.00,  "image": "fire.png"},
]

# ── Placeholder Inventory table data ─────────────────────────────────
_inventory = [
    {
        "itemID": 1,
        "name": "Duck Spell",
        "description": "...",
        "format": "Tome",
        "potency": 3,
        "reusable": "0",
        "category": "Conjuration",
        "price": 150.25,
        "amount": 7,
        "base_info": 1,
    },
    {
        "itemID": 2,
        "name": "Duck Spell",
        "description": "...",
        "format": "PDF",
        "potency": 7,
        "reusable": "",
        "category": "Conjuration",
        "price": 277.55,
        "amount": 3,
        "base_info": 1,
    },
    {
        "itemID": 3,
        "name": "Duck Spell",
        "description": "...",
        "format": "Scroll",
        "potency": 6,
        "reusable": "1",
        "category": "Conjuration",
        "price": 245.50,
        "amount": 8,
        "base_info": 1,
    },
    {
        "itemID": 4,
        "name": "Other Spell",
        "description": "...",
        "format": "PDF",
        "potency": 6,
        "reusable": "0",
        "category": "Protection",
        "price": 200.50,
        "amount": 4,
        "base_info": 2,
    },
]


def get_all_items() -> list[dict]:
    """Return every item in the catalogue."""
    return list(_baseprice)


def get_all_items_by_id(item_id: int) -> list[dict]:
    """Return ALL inventory items where base_info matches the given id."""
    return [item for item in _inventory if item["base_info"] == item_id]


def get_item_by_id(item_id: int) -> dict | None:
    """Look up a single item.  Returns None when not found."""
    return next((i for i in _inventory if i["base_info"] == item_id), None)
