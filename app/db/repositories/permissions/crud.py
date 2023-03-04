from app.db.repositories.common import BaseCrud
from app.db.repositories.permissions.model import Permissions

from app.models.domain import PermissionsInDB

from app.models.domain.perms import Permissions as PermissionsInCreate


class PermissionsCrud(BaseCrud[Permissions, PermissionsInCreate, PermissionsInDB]):
	model = Permissions
