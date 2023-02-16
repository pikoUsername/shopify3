from typing import Optional

import sqlalchemy as sa

from app.db.repositories.common import BaseCrud
from app.models.domain.users import UserInDB
from app.models.schemas.users import UserInCreate, UserInUpdate
from app.services.security import get_password_hash, verify_password

from .model import Users


__all__ = "UserCrud",


class UserCrud(BaseCrud[Users, UserInCreate, UserInUpdate]):
	model = Users

	@classmethod
	async def get_by_email(cls, db, email: str) -> Optional[Users]:  # noqa
		return await db.execute(
			sa.select(Users).where(Users.email == email).scalar())

	@classmethod
	async def get_by_username(cls, db, username: str) -> Optional[Users]:
		return await db.execute(
			sa.select(cls.model).where(Users.username == username).scalar())

	@classmethod
	async def update_user(cls, db, db_user: UserInUpdate, current_user: UserInUpdate) -> Users:
		if isinstance(current_user, dict):
			update_data = current_user
		else:
			update_data = current_user.dict(exclude_unset=True)
		if update_data["password"]:
			hashed_password = get_password_hash(update_data["password"])
			del update_data["password"]
			update_data["password_hash"] = hashed_password
		db_user = await cls.get_by_email(db, db_user.email)
		return await super().update(db, db_obj=db_user, obj_in=update_data)

	@classmethod
	async def authenticate(cls, db, *, email: str, password: str) -> Optional[Users]:
		user = await cls.get_by_email(db, email=email)
		if not user:
			return None
		if not verify_password(password, user.hashed_password):
			return None
		return user
