"""Logon request/response models."""
from typing import Optional
from pydantic import BaseModel, Field


class LogonRequest(BaseModel):
    """Request model for customer logon."""

    model_config = {"populate_by_name": True}
    email: str
    pass_: str = Field(alias="pass")


class LogonResponse(BaseModel):
    """Response model for customer logon."""

    status: str
    customerid: Optional[int] = None

