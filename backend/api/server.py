"""
API route aggregation – collects all sub-routers into one top-level router.
"""
from fastapi import APIRouter
from api.routes.auth import router as auth_router
from api.routes.inventory import router as inventory_router
from api.routes.purchase import router as purchase_router
from api.routes.health import router as health_router
from api.routes.credit_card import router as credit_card_router
from api.routes.address import router as address_router
from api.routes.user import router as user_router

router = APIRouter()

router.include_router(auth_router)
router.include_router(inventory_router)
router.include_router(purchase_router)
router.include_router(health_router)
router.include_router(credit_card_router)
router.include_router(address_router)
router.include_router(user_router)
