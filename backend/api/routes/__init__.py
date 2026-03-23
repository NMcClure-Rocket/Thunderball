"""Routes package"""
from .auth import router as auth_router
from .inventory import router as inventory_router
from .purchase import router as purchase_router
from .health import router as health_router
from .credit_card import router as credit_card_router
from .address import router as address_router
from .user import router as user_router

__all__ = [
    "auth_router",
    "inventory_router",
    "purchase_router",
    "health_router",
    "credit_card_router",
    "address_router",
    "user_router",
]
