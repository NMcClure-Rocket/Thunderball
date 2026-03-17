"""Address request/response models."""
from pydantic import BaseModel


class NewAddressRequest(BaseModel):
    first_name: str
    last_name: str
    address: str
    addr_2: str
    city: str
    state: str
    country: str
    zip: str
