"""Credit card routes."""
from fastapi import APIRouter, HTTPException
from api.models.credit_card import NewCCRequest
from api.services.credit_card_service import get_cards_by_customer, create_card

router = APIRouter()


@router.post("/newcc")
async def new_credit_card(body: NewCCRequest):
    create_card(customer_id=0, card_data=body.model_dump())
    return {"status": "ok"}


@router.get("/getcc/{customer_id}")
async def get_credit_cards(customer_id: int):
    cards = get_cards_by_customer(customer_id)
    return {"rows": cards}
