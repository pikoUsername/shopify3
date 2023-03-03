from typing import List, TYPE_CHECKING

from .rwschema import RWSchema

# if TYPE_CHECKING:
from app.models.domain import CommentInDB
from app.models.domain import SellerInDB
from app.models.domain import TagsInDB
from app.models.domain import TextEntitiesInDB


class ProductInResponse(RWSchema):
	name: str
	seller_id: int
	comments: List["CommentInDB"] = []
	tags: List["TagsInDB"] = []
	watches: int = 0
	description: str
	text_entities: List["TextEntitiesInDB"] = []


class ProductInCreate(RWSchema):
	name: str
	seller: "SellerInDB"
	seller_id: "SellerInDB"
	tags: List["TagsInDB"]
	description: str


class ProductInUpdate(RWSchema):
	name: str
	description: str
	tags: List["TagsInDB"] = []
