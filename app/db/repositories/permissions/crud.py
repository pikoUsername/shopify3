from app.db.repositories.common import BaseCrud
from app.db.repositories.permissions.model import Permissions

from app.models.domain import PermissionsInDB

from app.db.repositories.user import Users


class PermissionsCrud(BaseCrud[Permissions, PermissionsInDB, PermissionsInDB]):
	model = Permissions
	# TODO: replace stub with actual model
	@classmethod
	async def create_for_user(cls, user: Users) -> Permissions:
		perms = Permissions(code=user.control.include("read edit delete"))
		return perms
