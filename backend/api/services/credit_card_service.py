"""
Credit card service – in-memory placeholder storage until Db2 is ready.
"""

_credit_cards: list[dict] = [
    {
        "id": 1,
        "customer_id": 1,
        "number": 11111111,
        "security_code": 111,
        "expiration": "12/12",
        "processor": "Visa",
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


def get_cards_by_customer(customer_id: int) -> list[dict]:
    """Return all credit cards for a given customer."""
    return [
        {k: v for k, v in cc.items() if k not in ("id", "customer_id")}
        for cc in _credit_cards
        if cc["customer_id"] == customer_id
    ]


def create_card(customer_id: int, card_data: dict) -> None:
    """Add a new credit card record."""
    global _next_id
    _credit_cards.append({"id": _next_id, "customer_id": customer_id, **card_data})
    _next_id += 1
