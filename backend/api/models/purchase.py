"""Purchase request/response models."""
from pydantic import BaseModel


class PurchaseRequest(BaseModel):
    itemId: int
    qty: int
    customerid: int
    addressid: int
    ccid: int
