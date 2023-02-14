import sqlalchemy as sa

from app.db.repositories.base import BaseModel


class Permissions(BaseModel):
	"""
	Все пермишинны будут привязаны к юзеру
	"""
	__tablename__ = "permissions"

	code = sa.Column(sa.String(256), nullable=False)  # format: {model_name}_{permission}
