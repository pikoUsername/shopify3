import typing

from fastapi import Depends, HTTPException
import sqlalchemy as sa
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.status import HTTP_403_FORBIDDEN

from app.api.dependencies.database import get_connection
from app.db.repositories.user import Users
from app.api.dependencies.authentication import get_current_user_authorizer
from app.core.config import get_app_settings
from app.core.settings.app import AppSettings
from app.db.repositories.groups import Groups
from app.db.repositories.control import AccessControl
from app.resources import strings


class CheckPermission:
	__slots__ = ("permissions", "model", "_access_control", "group", "_perm_code")

	def __init__(
		self,
		permission: str,
		model: typing.Union[str, sa.Table] = None,
		group: typing.Union[str, Groups] = None
	) -> None:
		"""
		:param permission: could be split by spaces
		:param model: init method takes table name and
		formates it into permission string that uses
		:param group:
		"""
		self.permissions = permission.split()
		if isinstance(model, sa.Table):
			model = getattr(model, "__tablename__") or model.__name__
		self.model = model
		self._access_control = AccessControl(self.model)
		self._perm_code = self._access_control.format(*self.permissions)
		if isinstance(group, Groups):
			group = group.name
		else:
			group = group
		self.group = group

	async def __call__(
		self,
		session: AsyncSession = Depends(get_connection),
		user: Users = Depends(get_current_user_authorizer(required=True)),
		settings: AppSettings = Depends(get_app_settings),
	) -> None:
		"""
		Will raise HTTPForbidden if user permissions not enough to use this route

		* Note: for frontend part, if user is not authed and has anonymous status
		  then redirect him to login page, and save first url somewhere

		:param session:
		:param user:
		:param settings:
		:return:
		"""
		not_enough_permissions = HTTPException(
			status_code=HTTP_403_FORBIDDEN,
			detail=strings.NOT_ENOUGH_PERMISSIONS,
		)
		if not self.group:
			group = session.query(Groups).filter(
				user.groups.any(Groups.name == self.group)
			)
			if group.name != self.group:
				raise not_enough_permissions

		if not user.check_permissions(" ".join(self._perm_code)):
			raise not_enough_permissions
