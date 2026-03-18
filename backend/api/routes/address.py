"""Address routes."""
from fastapi import APIRouter
from api.models.address import NewAddressRequest
from api.services.address_service import get_addresses_by_customer, create_address

router = APIRouter()


@router.post("/newaddress")
async def new_address(body: NewAddressRequest):
    create_address(customer_id=0, address_data=body.model_dump())
    return {"status": "ok"}


@router.get("/getaddress/{customer_id}")
async def get_addresses(customer_id: int):
    addresses = get_addresses_by_customer(customer_id)
    return {"rows": addresses}
