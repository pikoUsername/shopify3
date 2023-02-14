import datetime
import uuid
import typing

import sqlalchemy as sa
from sqlalchemy import func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.db.repositories.base import BaseModel
from app.db.repositories.helpers import UserToGroups
from app.models.domain.perms import PermissionsInDB
from app.services.security import verify_password, get_password_hash, generate_salt


class Users(BaseModel):
	__tablename__ = "users"

	username = sa.Column(
		sa.String(255), index=True, primary_key=True, nullable=False, unique=True)
	uuid = sa.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
	lastname = sa.Column(sa.String(255))
	last_online = sa.Column(sa.DateTime(), server_default=func.now())
	email = sa.Column(sa.String(320), index=True, nullable=False)
	is_stuff = sa.Column(sa.Boolean, default=False)
	image_url = sa.Column(sa.String(256))
	bio = sa.Column(sa.String(256))
	address = sa.Column(sa.String(256))
	encrypted_password = sa.Column(sa.String(300), nullable=False)
	salt = sa.Column(sa.String(256), nullable=False)
	permissions = relationship("Permissions", uselist=False, back_populates="users")
	groups = relationship("Groups", back_populates="users", secondary=UserToGroups)
	seller = relationship("Seller", back_populates="users")
	is_deactivated = sa.Column(sa.Boolean)

	def __init__(self, password=None, password_hash=None, salt=None, **kwargs) -> None:
		if salt is None:
			salt = generate_salt()
		self.salt = salt
		if password_hash is None and password is not None:
			password_hash = get_password_hash(self.salt + password)

		super().__init__(encrypted_password=password_hash, **kwargs)

	def change_name(self, username):
		"""
		Изменяет только lastname так как username является ID юзера
		"""
		if not self.lastname:
			self.lastname = username
		self.lastname = username

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

	def get_group_perms(self) -> typing.Set[str]:
		result: typing.Set[str] = set()
		for group in self.groups:
			for perm in group.permissions:
				result.add(perm.code.split())

		return result

	def get_permissions(self) -> typing.Set[str]:
		result = set()

		for perm in self.permissions:
			result.add(perm.code.split())

		return result

	def get_all_permissions(self) -> typing.Set[str]:
		return {
			*self.get_group_perms(),
			*self.get_permission(),
		}

	def check_permissions(self, code: str) -> bool:
		"""
		Format: {model_name}_{permissions}
		"""
		perms = self.get_all_permissions()
		return code in perms
