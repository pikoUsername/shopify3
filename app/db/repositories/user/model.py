import datetime

import sqlalchemy as sa
from sqlalchemy import func
from sqlalchemy.orm import relationship

from app.db.repositories.base import BaseModel
from app.services.security import verify_password, get_password_hash, generate_salt


class Users(BaseModel):
	__tablename__ = "users"

	username = sa.Column(
		sa.String(255), index=True, primary_key=True, nullable=False, unique=True)
	lastname = sa.Column(sa.String(255))
	last_online = sa.Column(sa.DateTime(), server_default=func.now())
	email = sa.Column(sa.String(320), index=True, nullable=False)
	is_stuff = sa.Column(sa.Boolean, default=False)
	bio = sa.Column(sa.String(256))
	address = sa.Column(sa.String(256))
	encrypted_password = sa.Column(sa.String(300), nullable=False)
	salt = sa.Column(sa.String(256), nullable=False)

	def __init__(self, password=None, password_hash=None, salt=None, **kwargs) -> None:
		if salt is not None:
			self.salt = salt
		if password_hash is None and password is not None:
			password_hash = get_password_hash(self.salt + password)

		super().__init__(encrypted_password=password_hash, **kwargs)

	@property
	def password(self):
		raise AttributeError("Password is write only")

	@password.setter
	def password(self, password: str) -> None:
		self.encrypted_password = get_password_hash(self.salt + password)

	def verify_password(self, password: str) -> bool:
		return verify_password(self.salt + password, self.encrypted_password)

	async def update_last_online(self) -> None:
		self.last_online = datetime.datetime.now()
