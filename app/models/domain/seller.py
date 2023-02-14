from typing import List

from pydantic import Field

from .rwmodel import RWModel
from ..common import DateTimeModelMixin, IDModelMixin


class SellerInDB(RWModel, IDModelMixin, DateTimeModelMixin):
	rating: int = Field(None)
	products: List["ProductInDB"] = []
	country: str
	bio: str
	is_activated: bool = Field(default=True)
	is_blocked = Field(default=False)
