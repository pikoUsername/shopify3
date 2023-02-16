from fastapi import APIRouter

from . import auth, users


router = APIRouter(tags=['user'])

router.include_router(auth.router, prefix="/profile")
router.include_router(users.router, prefix="/user")
