from typing import TYPE_CHECKING

from pydantic import Field

from .rwmodel import RWModel
from ..common import IDModelMixin, DateTimeModelMixin

if TYPE_CHECKING:
	from .users import UserInDB
	from .text_entities import TextEntitiesInDB


class CommentInDB(IDModelMixin, DateTimeModelMixin, RWModel):
	author: "UserInDB"
	author_id: int
	content: str = Field(max_length=256)
	text_entities: list["TextEntitiesInDB"] = []
