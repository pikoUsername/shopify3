from fastapi import APIRouter

from . import product, seller


router = APIRouter()

router.include_router(product.router, prefix="/product")
router.include_router(seller.router, prefix="/seller")
