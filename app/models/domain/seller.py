from typing import List, TYPE_CHECKING

from pydantic import Field

from .rwmodel import RWModel
from ..common import DateTimeModelMixin, IDModelMixin


if TYPE_CHECKING:
	from .products import ProductInDB


class SellerInDB(RWModel, IDModelMixin, DateTimeModelMixin):
	rating: int = Field(None)
	products: List["ProductInDB"] = []
	country: str
	bio: str
	is_activated: bool = Field(default=True)
	is_blocked: bool = Field(default=False)
