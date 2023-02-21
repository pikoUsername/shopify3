from sqlalchemy.ext.asyncio import AsyncSession

from app.models.domain.comments import CommentInDB
from app.models.schemas.comment import CommentInCreate
from app.services.text_entities import parse_text
from ..common import BaseCrud
from .model import Comments

from app.db.repositories.text_entities import TextEntitiesCRUD
from app.db.repositories.user import UserCrud


class CommentsCRUD(BaseCrud[Comments, CommentInCreate, CommentInDB]):
	model = Comments

	@classmethod
	async def create(cls, db: AsyncSession, obj_in: CommentInCreate) -> Comments:
		# filters garbage, and raises error if it contains unwanted html tags
		# gives list of entities
		text, entities = parse_text(obj_in.text)
		entities = await TextEntitiesCRUD.create_list(db, entities)
		author, _ = await UserCrud.get_or_create(db, obj_in.author_id)
		obj_in.text = ""
		comment = await CommentsCRUD.create_with_relationship(
			db, obj_in, {'entities': entities, 'author': author}
		)
		return comment
