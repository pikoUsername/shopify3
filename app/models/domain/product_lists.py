from pydantic import Field

from .products import ProductInDB
from .rwmodel import RWModel


class ProductListInDB(RWModel):
	name: str = Field(max_length=52)
	products: list[ProductInDB] = []
