"""Purchase request/response models."""
from pydantic import BaseModel


class PurchaseRequest(BaseModel):
    """Request model for submitting a purchase order."""

    model_config = {"populate_by_name": True}
    itemid: int
    qty: int
    transaction: float
    customerid: int
    addressid: int
    ccid: int

