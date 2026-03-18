"""Authentication routes."""
from fastapi import APIRouter
from api.models.logon import LogonRequest

router = APIRouter()


@router.post("/logon")
async def logon(body: LogonRequest):
    return {"status": "ok", "user": body.user}
