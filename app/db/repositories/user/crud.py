from typing import Optional

import sqlalchemy as sa

from app.db.repositories.common import BaseCrud
from app.models.domain.users import User, UserInDB
from app.models.schemas.users import UserInCreate, UserInUpdate
from app.services.security import get_password_hash, verify_password

from .model import Users


__all__ = "UserCrud",


class userCrud(BaseCrud[Users, UserInCreate, UserInUpdate]):
	async def get_by_email(self, db, email: str) -> Optional[Users]:  # noqa
		return await db.execute(
			sa.select(Users).where(Users.email == email).scalar())

	async def get_by_username(self, db, username: str) -> Optional[Users]:
		return await db.execute(
			sa.select(self.model).where(Users.username == username).scalar())

	async def update_user(self, db, db_user: User, current_user: UserInUpdate) -> Users:
		if isinstance(current_user, dict):
			update_data = current_user
		else:
			update_data = current_user.dict(exclude_unset=True)
		if update_data["password"]:
			hashed_password = get_password_hash(update_data["password"])
			del update_data["password"]
			update_data["password_hash"] = hashed_password
		db_user = await self.get_by_email(db, db_user.email)
		return await super().update(db, db_obj=db_user, obj_in=update_data)

	async def authenticate(self, db, *, email: str, password: str) -> Optional[User]:
		user = await self.get_by_email(db, email=email)
		if not user:
			return None
		if not verify_password(password, user.hashed_password):
			return None
		return user


UserCrud: userCrud = userCrud(Users)
