"""Credit card request/response models."""
from pydantic import BaseModel


class NewCCRequest(BaseModel):  # pylint: disable=duplicate-code
    """Request model for creating a new credit card entry."""

    model_config = {"populate_by_name": True}
    number: int
    security_code: int
    expiration: str
    processor: str
    first_name: str
    last_name: str
    address: str
    addr_2: str
    city: str
    state: str
    country: str
    zip: str
    customerid: int
