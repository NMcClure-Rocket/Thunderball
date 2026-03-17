"""Utility functions for serializing DB2 row tuples to JSON."""

import json
from typing import Any, List


def baseprice_json(rows: List[Any]) -> str:
    """Convert list of Db2 row tuples from BASEPRICE table into a JSON string.

    Each row is expected to have columns in this order:
        0: id, 1: name, 3: price, 4: image

    Args:
        rows: List of row tuples returned from a Db2 cursor.

    Returns:
        A JSON string with a top-level "items" key.
    """
    inner_json = []
    for row in rows:
        r = list(row)
        json_row = {"id": r[0], "name": r[1], "price": float(r[2]), "image": r[3]}
        inner_json.append(json_row)

    return json.dumps({"items": inner_json})


def inventory_json(rows: List[Any]) -> str:
    """Convert a list of Db2 row tuples from INVENTORY table into a JSON string.

    Each row is expected to have columns in this order:
        0: name, 1: description, 2: format, 3: potency,
        4: reusable, 5: category, 6: price, 7: amount

    Args:
        rows: List of row tuples returned from a Db2 cursor.

    Returns:
        A JSON string with a top-level "rows" key.
    """
    inner_json = []
    for row in rows:
        r = list(row)
        json_row = {
            "itemid": r[0],
            "name": r[1],
            "description": r[2],
            "format": r[3],
            "potency": r[4],
            "reusable": r[5],
            "category": r[6],
            "price": float(r[7]),
            "amount": r[8],
        }
        inner_json.append(json_row)

    return json.dumps({"rows": inner_json})
