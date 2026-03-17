"""Credit card request/response models."""
from pydantic import BaseModel


class NewCCRequest(BaseModel):
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
