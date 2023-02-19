from .rwschema import RWSchema
from ..domain.users import User


class CommentInCreate(RWSchema):
	author: User
	text: str
