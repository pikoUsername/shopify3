import sqlalchemy as sa

from .base import BaseModel


class UserToGroups(BaseModel):
	__tablename__ = "user_to_groups"

	user_id = sa.Column(sa.Integer, sa.ForeignKey("users.id"), nullable=False, primary_key=True)
	group_id = sa.Column(sa.Integer, sa.ForeignKey("groups.id"), nullable=False, primary_key=True)
