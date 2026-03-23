"""Health / heartbeat routes."""
import time
from fastapi import APIRouter

router = APIRouter()


@router.get("/pulse")
async def pulse():
    """Return server heartbeat with current timestamp."""
    return {"status": "ok", "timestamp": int(time.time() * 1000)}
