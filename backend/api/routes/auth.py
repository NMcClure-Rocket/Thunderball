"""Authentication routes."""
from fastapi import APIRouter
from api.models.logon import LogonRequest, LogonResponse

router = APIRouter()


@router.post("/logon", response_model=LogonResponse)
async def logon(body: LogonRequest):
    return LogonResponse(status="ok", customerid=None)
