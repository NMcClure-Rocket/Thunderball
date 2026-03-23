"""User creation routes."""
from fastapi import APIRouter, HTTPException
from api.models.user import CreateUserRequest
from api.services.auth_service import create_user

router = APIRouter()


@router.post("/createuser")
async def createuser(body: CreateUserRequest):
    """Create a new user account."""
    created = create_user(body.first_name, body.last_name, body.user, body.pass_)
    if not created:
        raise HTTPException(status_code=400, detail="Username already exists")
    return {"status": "ok"}
