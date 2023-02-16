from pydantic import Field

from .comments import CommentInDB
from .rwmodel import RWModel
from .seller import SellerInDB
from .tag import TagsInDB
from .text_entities import TextEntitiesInDB
from ..common import IDModelMixin, DateTimeModelMixin


class ProductInDB(IDModelMixin, DateTimeModelMixin, RWModel):
	name: str = Field(max_length=92)
	seller: SellerInDB = []
	seller_id: int
	comments: list[CommentInDB] = []
	tags: list[TagsInDB] = []
	watches: int
	description: str
	text_entities: list[TextEntitiesInDB] = []
