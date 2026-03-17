"""Logon request/response models."""
from pydantic import BaseModel, Field


class LogonRequest(BaseModel):
    model_config = {"populate_by_name": True}
    user: str
    pass_: str = Field(alias="pass")
