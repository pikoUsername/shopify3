from sqlalchemy.ext.asyncio import AsyncSession

from app.db.repositories.user import UserCrud, Users


async def check_email_is_taken(email: str) -> bool:
	result = await UserCrud.get_by_email(Users.email == email)
	return bool(result)


async def check_username_is_taken(username: str) -> bool:
	result = await UserCrud.get_by_username(username)
	return bool(result)
