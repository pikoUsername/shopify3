from typing import TYPE_CHECKING, List

from pydantic import Field

from app.models.common import IDModelMixin, DateTimeModelMixin

if TYPE_CHECKING:
	from app.models.domain.text_entities import TextEntitiesInDB
	from app.models.domain.users import UserInDB


class CommentSection(IDModelMixin, DateTimeModelMixin):
	author: "UserInDB"
	author_id: int
	content: str = Field(max_length=256)
	text_entities: List["TextEntitiesInDB"] = []
	likes: int = 0
