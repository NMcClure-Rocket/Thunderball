"""Authentication routes."""
from fastapi import APIRouter
from fastapi.responses import JSONResponse
from api.models.logon import LogonRequest
from api.services.auth_service import authenticate

router = APIRouter()


@router.post("/logon")
async def logon(body: LogonRequest):
    if not authenticate(body.user, body.pass_):
        return JSONResponse(
            status_code=401,
            content={"status": "error", "user": None},
        )
    return {"status": "ok", "user": body.user}
