"""Address routes."""
from typing import Any, Dict

from fastapi import APIRouter
from api.models.address import NewAddressRequest
# from api.services.address_service import get_addresses_by_customer, create_address
from db.connector import conn
from db.dao.shipping_address_dao import ShippingAddressDAO

router = APIRouter()


@router.post("/newaddress")
async def new_address(body: Dict[str, Any]):
    # create_address(customer_id=0, address_data=body.model_dump())
    # return {"status": "ok"}
    dao = ShippingAddressDAO(conn)
    rows = dao.insert_address(body)
    new_addressid = rows[0][0]
    return {"status": "ok", "addressid": new_addressid}


@router.get("/getaddress/{customer_id}")
async def get_addresses(customer_id: int):
    # addresses = get_addresses_by_customer(customer_id)
    # return {"rows": addresses}
    return
