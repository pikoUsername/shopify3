from typing import List, TYPE_CHECKING

import sqlalchemy as sa
from sqlalchemy.orm import relationship, declared_attr

from .base import BaseModel, TimedModel


if TYPE_CHECKING:
	from app.db.repositories.text_entities import TextEntity
	from app.db.repositories.user import Users


class UserToGroups(BaseModel):
	__tablename__ = "user_to_groups"

	user_id = sa.Column(sa.Integer, sa.ForeignKey("users.id"), nullable=False, primary_key=True)
	group_id = sa.Column(sa.Integer, sa.ForeignKey("groups.id"), nullable=False, primary_key=True)


class ListsToProducts(BaseModel):
	__tablename__ = 'lists_to_products'

	product_list_id = sa.Column(sa.Integer, sa.ForeignKey("product_lists.id"), nullable=False, primary_key=True)
	product_id = sa.Column(sa.Integer, sa.ForeignKey("products.id"), nullable=False, primary_key=True)


class CommentSection(TimedModel):
	"""
	Reusable comment columns, for reviews, comments, and etc.
	"""
	__abstract__ = True

	content = sa.Column(sa.String(256), nullable=False)
	likes = sa.Column(sa.Integer, default=0)

	@declared_attr
	def author_id(cls) -> "sa.Integer":
		return sa.Column(sa.Integer, sa.ForeignKey("users.id", ondelete="SET NULL"))

	@declared_attr
	def author(cls) -> "Users":
		return relationship(
			"Users",
			back_populates=cls.__tablename__ if hasattr(cls, '__tablename__') else cls.__name__.lower()
		)

	@declared_attr
	def text_entities(cls) -> List["TextEntity"]:
		return relationship(
			"TextEntities",
			back_populates=cls.__tablename__ if hasattr(cls, '__tablename__') else cls.__name__.lower()
		)
