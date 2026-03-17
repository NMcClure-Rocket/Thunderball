"""
Conftest for backend integration tests.

Patches the DB2 connection used by the inventory route so that the integration
tests run reliably without a live DB2 connection.  The fake rows mirror the
same in-memory data used by the inventory service.
"""
from unittest.mock import MagicMock, patch
import pytest

_FAKE_ROWS = [
    (1, "Duck Spell A", 9.99,  "duck-a.png"),
    (2, "Duck Spell B", 12.50, "duck-b.png"),
    (3, "Fire Spell",   5.00,  "fire.png"),
]


@pytest.fixture(autouse=True, scope="module")
def mock_inventory_db():
    """Patch api.routes.inventory.conn with a mock that returns known rows."""
    mock_cursor = MagicMock()
    mock_cursor.fetchall.return_value = _FAKE_ROWS

    mock_conn = MagicMock()
    mock_conn.cursor.return_value = mock_cursor

    with patch("api.routes.inventory.conn", mock_conn):
        yield
