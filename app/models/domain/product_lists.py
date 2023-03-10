from __future__ import annotations
from typing import TYPE_CHECKING, List

from pydantic import Field

from .rwmodel import RWModel
from ..common import IDModelMixin, DateTimeModelMixin

if TYPE_CHECKING:
	from .products import ProductInDB


class ProductListInDB(RWModel, IDModelMixin, DateTimeModelMixin):
	name: str = Field(max_length=52)
	products: List[ProductInDB] = []
