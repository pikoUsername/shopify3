from fastapi import APIRouter

from app.api.routes import users
from app.api.routes import auth
from .shop import api as shop


router = APIRouter()
router.include_router(shop.router, tags=["shop", "market"], prefix="/shop")
router.include_router(users.router, tags=["users"], prefix="/user")
router.include_router(auth.router, tags=["auth"], prefix="/auth")
