"""
Address service – in-memory placeholder storage until Db2 is ready.
"""  # pylint: disable=duplicate-code

_addresses: list[dict] = [
    {
        "id": 1,
        "customer_id": 1,
        "first_name": "John",
        "last_name": "Doe",
        "address": "5555 Street Rd.",
        "addr_2": "Apt E111",
        "city": "Orlando",
        "state": "FL",
        "country": "United States",
        "zip": "11111",
    },
]

_next_id = 2


def get_addresses_by_customer(customer_id: int) -> list[dict]:
    """Return all shipping addresses for a given customer."""
    return [
        {k: v for k, v in addr.items() if k not in ("id", "customer_id")}
        for addr in _addresses
        if addr["customer_id"] == customer_id
    ]


def create_address(customer_id: int, address_data: dict) -> None:
    """Add a new shipping address record."""
    global _next_id  # pylint: disable=global-statement
    _addresses.append({"id": _next_id, "customer_id": customer_id, **address_data})
    _next_id += 1

