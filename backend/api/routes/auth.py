"""Authentication routes."""
from fastapi import APIRouter, HTTPException
from api.models.logon import LogonRequest, LogonResponse
from db.connector import conn
from db.dao.customer_dao import CustomerDAO

router = APIRouter()


@router.post("/logon", response_model=LogonResponse)
async def logon(body: LogonRequest):
    try:
        dao = CustomerDAO(conn)
        customer = dao.get_customer_by_email_and_password(body.email, body.pass_)
        
        if customer:
            return LogonResponse(status="ok", customerid=customer[0])
        else:
            raise HTTPException(status_code=401, detail="Invalid email or password")
            
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error: {e}")
        raise HTTPException(status_code=500, detail="Database error")
