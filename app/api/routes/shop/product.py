from fastapi import APIRouter, Depends, Body
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.dependencies.database import get_connection
from app.db.repositories.product import ProductsCRUD
from app.models.schemas.product import ProductInResponse, ProductInCreate


router = APIRouter()


@router.get("/product/", name="products:get-product")
async def create_product(
		product_create: ProductInCreate = Body(..., embed=True, alias="product"),
		db: AsyncSession = Depends(get_connection),
) -> ProductInResponse:
	pass
