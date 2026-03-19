"""Purchase request/response models."""
from pydantic import BaseModel


class PurchaseRequest(BaseModel):
    model_config = {"populate_by_name": True}
    itemid: int
    qty: int
    transaction: float
    customerid: int
    addressid: int
    ccid: int
