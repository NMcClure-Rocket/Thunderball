"""
Conftest for backend integration tests.

Patches the DB2 connection used by the inventory route so that the integration
tests run reliably without a live DB2 connection.  The fake rows mirror the
same in-memory data used by the inventory service.
"""
from unittest.mock import MagicMock, patch
import pytest
import api.routes.address  # noqa: F401 – ensure module is imported before patching

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


_SAMPLE_ADDRESS_ROW = (1, "Jane", "Doe", "1 Main St", "", "Miami", "FL", "US", "33101", 1)


@pytest.fixture(autouse=True, scope="module")
def mock_address_db():
    """Patch api.routes.address.conn so address route tests need no live DB."""
    mock_conn = MagicMock()

    def make_cursor():
        cursor = MagicMock()

        def do_execute(sql, params=None):
            sql_upper = sql.upper()
            if "COUNT(*)" in sql_upper:
                cursor.fetchall.return_value = [(0,)]
            elif sql_upper.strip().startswith("INSERT"):
                cursor.fetchall.return_value = []
            elif params and len(params) == 1 and "ADDRESSID" in sql_upper:
                # Final SELECT after INSERT: SELECT * WHERE ADDRESSID = ?
                cursor.fetchall.return_value = [_SAMPLE_ADDRESS_ROW]
            elif params and len(params) == 1:
                # get_records_by_customerid: SELECT * WHERE CUSTOMERID = ?
                cursor.fetchall.return_value = (
                    [] if params[0] == 9999 else [_SAMPLE_ADDRESS_ROW]
                )
            else:
                # Dedup SELECT (many params) – no existing record
                cursor.fetchall.return_value = []

        cursor.execute.side_effect = do_execute
        return cursor

    mock_conn.cursor.side_effect = make_cursor

    with patch("api.routes.address.conn", mock_conn):
        yield
