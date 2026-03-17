"""
Conftest for backend integration tests.

Patches the DB2 connection used by the inventory route so that the integration
tests run reliably without a live DB2 connection.  The fake rows mirror the
same in-memory data used by the inventory service.
"""
from unittest.mock import MagicMock, patch
import pytest

# 4-column rows for BasePriceDAO.get_all_records() → used by GET /inventory
_BASE_PRICE_ROWS = [
    (1, "Duck Spell A", 9.99,  "duck-a.png"),
    (2, "Duck Spell B", 12.50, "duck-b.png"),
    (3, "Fire Spell",   5.00,  "fire.png"),
]

# 9-column rows for InventoryDAO.get_item_by_baseinfo() → used by GET /inventory/{item_id}
_INVENTORY_ITEM_ROWS = {
    1: [(1, "Duck Spell A", "A duck-based spell", "instant", 5, True, "offensive", 9.99, 10)],
    2: [(2, "Duck Spell B", "Another duck spell", "channel", 3, False, "defensive", 12.50, 5)],
    3: [(3, "Fire Spell",   "Burns things",        "instant", 7, True, "offensive",  5.00, 8)],
}


@pytest.fixture(autouse=True, scope="module")
def mock_inventory_db():
    """Patch api.routes.inventory.conn with a smart mock.

    BasePriceDAO.get_all_records() passes no params → returns 4-column rows.
    InventoryDAO.get_item_by_baseinfo() passes (item_id,) → returns 9-column rows.
    """
    mock_conn = MagicMock()

    def make_cursor():
        cursor = MagicMock()

        def do_execute(sql, params=None):
            if params:
                item_id = params[0]
                cursor.fetchall.return_value = _INVENTORY_ITEM_ROWS.get(item_id, [])
            else:
                cursor.fetchall.return_value = _BASE_PRICE_ROWS

        cursor.execute.side_effect = do_execute
        return cursor

    mock_conn.cursor.side_effect = make_cursor

    with patch("api.routes.inventory.conn", mock_conn):
        yield
