"""
Pydantic models / DTOs
"""
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class ExampleRequest(BaseModel):
    """Example request model"""
    name: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = None
    value: int = Field(ge=0)

class ExampleResponse(BaseModel):
    """Example response model"""
    id: str
    name: str
    description: Optional[str]
    value: int
    created_at: datetime
    
    class Config:
        from_attributes = True
