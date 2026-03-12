"""
Example route module
"""

from fastapi import APIRouter, HTTPException
from typing import List

router = APIRouter()


@router.get("/example")
async def get_example():
    """Example endpoint"""
    return {"message": "This is an example endpoint"}


@router.post("/example")
async def create_example(data: dict):
    """Create example"""
    return {"message": "Example created", "data": data}
