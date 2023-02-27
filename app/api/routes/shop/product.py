from fastapi import APIRouter, Depends, Body, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.dependencies.database import get_connection
from app.api.dependencies.permissions import CheckPermission
from app.db.repositories.product import ProductsCRUD, Products
from app.db.repositories.seller import SellerCRUD
from app.models.schemas.product import ProductInResponse, ProductInCreate
from app.resources.strings import DUPLICATE_ERROR
from app.services.text_entities import Parser
from app.db.repositories.text_entities import TextEntitiesCRUD


router = APIRouter()


@router.post(
	"/product/",
	name="products:create-product",
	dependencies=[Depends(CheckPermission("*", Products.__tablename__))]
)
async def create_product(
		product_create: ProductInCreate = Body(..., embed=True, alias="product"),
		db: AsyncSession = Depends(get_connection),
) -> ProductInResponse:
	seller = await SellerCRUD.get_by_kwargs(
		db, id=product_create.seller_id
	)
	if product := await ProductsCRUD.get_by_kwargs(db, seller_id=seller.id, name=product_create.name):
		raise HTTPException(
			detail=DUPLICATE_ERROR.format(
				model=Products.__tablename__,
				id=product.id
			),
			status_code=400,
		)
	parsed_entities = Parser().parse_entities(product_create.description)
	parsed_entities = await TextEntitiesCRUD.create_list(db, parsed_entities)
	relations = {"seller": seller, "comments": [], "text_entities": parsed_entities}
	product = await ProductsCRUD.create_with_relationship(db, product_create, relations)
	return ProductInResponse(
		name=product.name,
		description=product.description,
		seller_id=seller.id,
		text_entities=parsed_entities,
	)
