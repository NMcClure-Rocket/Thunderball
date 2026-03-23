"""Credit card routes."""
from fastapi import APIRouter
from api.models.credit_card import NewCCRequest
from db.connector import conn
from db.dao.cci_dao import CCIDao

router = APIRouter()


@router.post("/newcc")
async def new_credit_card(body: NewCCRequest):
    """Create a new credit card record."""
    # create_card(customer_id=0, card_data=body.model_dump())
    # return {"status": "ok"}
    dao = CCIDao(conn)
    rows = dao.insert_cc(body)
    new_ccid = rows[0][0]
    return {"status": "ok", "ccid": new_ccid}


@router.get("/getcc/{customer_id}")
async def get_credit_cards(customer_id: int):  # pylint: disable=unused-argument
    """Retrieve all credit cards for a customer (stub)."""
    # cards = get_cards_by_customer(customer_id)
    # return {"rows": cards}
    return
