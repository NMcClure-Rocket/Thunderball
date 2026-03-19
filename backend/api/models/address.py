"""Address request/response models."""
from pydantic import BaseModel


class NewAddressRequest(BaseModel):
    model_config = {"populate_by_name": True}
    first_name: str
    last_name: str
    address: str
    addr_2: str
    city: str
    state: str
    country: str
    zip: str
    customerid: int