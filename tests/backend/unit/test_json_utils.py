"""Unit tests for api/utils/json_utils.py"""

import json
import pytest
from api.utils.json_utils import init_json


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

class TestInitJson:
    def test_returns_valid_json_string(self):
        result = init_json([_make_row()])
        parsed = json.loads(result)
        assert isinstance(parsed, dict)

    def test_top_level_key_is_rows(self):
        result = init_json([_make_row()])
        parsed = json.loads(result)
        assert "rows" in parsed

    def test_single_row_mapped_correctly(self):
        row = _make_row(
            name="Ice Spell", description="Freezes", fmt="channel",
            potency=3, reusable=False, category="defensive",
            price="14.50", amount=2,
        )
        parsed = json.loads(init_json([row]))
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
        parsed = json.loads(init_json([row]))
        assert isinstance(parsed["rows"][0]["price"], float)
        assert parsed["rows"][0]["price"] == 7.0

    def test_price_already_float_stays_float(self):
        row = _make_row(price=5.0)
        parsed = json.loads(init_json([row]))
        assert isinstance(parsed["rows"][0]["price"], float)

    def test_multiple_rows_all_present(self):
        rows = [_make_row(name="Spell A"), _make_row(name="Spell B")]
        parsed = json.loads(init_json(rows))
        assert len(parsed["rows"]) == 2
        assert parsed["rows"][0]["name"] == "Spell A"
        assert parsed["rows"][1]["name"] == "Spell B"

    def test_empty_rows_returns_empty_list(self):
        parsed = json.loads(init_json([]))
        assert parsed == {"rows": []}

    def test_invalid_price_raises_value_error(self):
        row = _make_row(price="not-a-number")
        with pytest.raises(ValueError):
            init_json([row])
