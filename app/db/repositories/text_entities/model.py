import sqlalchemy as sa
from sqlalchemy.orm import relationship

from app.db.repositories.base import BaseModel


class TextEntity(BaseModel):
	"""
	Used for messages, comments, and etc.
	offset uses for define start text entity
	length uses for defining ending of the text entity
	In one message could be a several text entities
	"""
	__tablename__ = "text_entities"

	type = sa.Column(sa.String(52), nullable=False)
	url = sa.Column(sa.Text)
	offset = sa.Column(sa.Integer, nullable=False)
	length = sa.Column(sa.Integer, nullable=False)
