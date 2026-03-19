"""Logon request/response models."""
from typing import Optional
from pydantic import BaseModel, Field


class LogonRequest(BaseModel):
    model_config = {"populate_by_name": True}
    email: str
    pass_: str = Field(alias="pass")


class LogonResponse(BaseModel):
    status: str
    customerid: Optional[int]
