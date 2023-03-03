from typing import TYPE_CHECKING

from .rwschema import RWSchema

if TYPE_CHECKING:
	from app.models.domain import User


class CommentInCreate(RWSchema):
	author: User
	text: str
