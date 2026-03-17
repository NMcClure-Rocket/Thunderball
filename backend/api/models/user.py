"""User request/response models."""
from pydantic import BaseModel, Field


class CreateUserRequest(BaseModel):
    model_config = {"populate_by_name": True}
    first_name: str
    last_name: str
    user: str
    pass_: str = Field(alias="pass")
