from .rwschema import RWSchema

from app.models.domain import User


class CommentInCreate(RWSchema):
	author: User
	text: str
