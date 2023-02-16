import sqlalchemy as sa

from .base import BaseModel


class UserToGroups(BaseModel):
	__tablename__ = "user_to_groups"

	user_id = sa.Column(sa.Integer, sa.ForeignKey("users.id"), nullable=False, primary_key=True)
	group_id = sa.Column(sa.Integer, sa.ForeignKey("groups.id"), nullable=False, primary_key=True)


class ListsToProducts(BaseModel):
	__tablename__ = 'lists_to_products'

	product_list_id = sa.Column(sa.Integer, sa.ForeignKey("product_lists.id"), nullable=False, primary_key=True)
	product_id = sa.Column(sa.Integer, sa.ForeignKey("products.id"), nullable=False, primary_key=True)
