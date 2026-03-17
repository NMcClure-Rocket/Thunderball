"""Unit tests for api/utils/json_utils.py"""

import json
import pytest
from api.utils.json_utils import inventory_json, baseprice_json


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _make_row(name="Fire Spell", description="Burns things", fmt="instant",
              potency=5, reusable=True, category="offensive",
              price="9.99", amount=10):
    return (name, description, fmt, potency, reusable, category, price, amount)


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------

class TestInventoryJson:
    def test_returns_valid_json_string(self):
        result = inventory_json([_make_row()])
        parsed = json.loads(result)
        assert isinstance(parsed, dict)

    def test_top_level_key_is_rows(self):
        result = inventory_json([_make_row()])
        parsed = json.loads(result)
        assert "rows" in parsed

    def test_single_row_mapped_correctly(self):
        row = _make_row(
            name="Ice Spell", description="Freezes", fmt="channel",
            potency=3, reusable=False, category="defensive",
            price="14.50", amount=2,
        )
        parsed = json.loads(inventory_json([row]))
        record = parsed["rows"][0]
        assert record["name"] == "Ice Spell"
        assert record["description"] == "Freezes"
        assert record["format"] == "channel"
        assert record["potency"] == 3
        assert record["reusable"] is False
        assert record["category"] == "defensive"
        assert record["price"] == 14.50
        assert record["amount"] == 2

    def test_price_is_coerced_to_float(self):
        row = _make_row(price="7")
        parsed = json.loads(inventory_json([row]))
        assert isinstance(parsed["rows"][0]["price"], float)
        assert parsed["rows"][0]["price"] == 7.0

    def test_price_already_float_stays_float(self):
        row = _make_row(price=5.0)
        parsed = json.loads(inventory_json([row]))
        assert isinstance(parsed["rows"][0]["price"], float)

    def test_multiple_rows_all_present(self):
        rows = [_make_row(name="Spell A"), _make_row(name="Spell B")]
        parsed = json.loads(inventory_json(rows))
        assert len(parsed["rows"]) == 2
        assert parsed["rows"][0]["name"] == "Spell A"
        assert parsed["rows"][1]["name"] == "Spell B"

    def test_empty_rows_returns_empty_list(self):
        parsed = json.loads(inventory_json([]))
        assert parsed == {"rows": []}

    def test_invalid_price_raises_value_error(self):
        row = _make_row(price="not-a-number")
        with pytest.raises(ValueError):
            inventory_json([row])


# ===========================================================================
# baseprice_json
# ===========================================================================

class TestBasePriceJson:
    def _row(self, id_=1, name="Duck Spell A", price=9.99, image="duck-a.png"):
        return (id_, name, price, image)

    def test_returns_string(self):
        result = baseprice_json([self._row()])
        assert isinstance(result, str)

    def test_returns_valid_json(self):
        result = baseprice_json([self._row()])
        parsed = json.loads(result)
        assert isinstance(parsed, dict)

    def test_top_level_key_is_items(self):
        parsed = json.loads(baseprice_json([self._row()]))
        assert "items" in parsed

    def test_single_row_id_mapped(self):
        parsed = json.loads(baseprice_json([(2, "Spell B", 12.5, "b.png")]))
        assert parsed["items"][0]["id"] == 2

    def test_single_row_name_mapped(self):
        parsed = json.loads(baseprice_json([(2, "Spell B", 12.5, "b.png")]))
        assert parsed["items"][0]["name"] == "Spell B"

    def test_single_row_price_mapped(self):
        parsed = json.loads(baseprice_json([(2, "Spell B", 12.5, "b.png")]))
        assert parsed["items"][0]["price"] == 12.5

    def test_single_row_image_mapped(self):
        parsed = json.loads(baseprice_json([(2, "Spell B", 12.5, "b.png")]))
        assert parsed["items"][0]["image"] == "b.png"

    def test_price_coerced_to_float(self):
        parsed = json.loads(baseprice_json([(1, "Test", "9", "img.png")]))
        assert isinstance(parsed["items"][0]["price"], float)

    def test_multiple_rows_all_present(self):
        rows = [(1, "A", 1.0, "a.png"), (2, "B", 2.0, "b.png")]
        parsed = json.loads(baseprice_json(rows))
        assert len(parsed["items"]) == 2

    def test_multiple_rows_order_preserved(self):
        rows = [(1, "A", 1.0, "a.png"), (2, "B", 2.0, "b.png")]
        parsed = json.loads(baseprice_json(rows))
        assert parsed["items"][0]["id"] == 1
        assert parsed["items"][1]["id"] == 2

    def test_empty_rows_returns_empty_items_list(self):
        parsed = json.loads(baseprice_json([]))
        assert parsed == {"items": []}
