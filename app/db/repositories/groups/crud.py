from app.db.repositories.common import BaseCrud
from app.models.domain import GroupInDB
from .model import Groups


class GroupsCRUD(BaseCrud[Groups, GroupInDB, GroupInDB]):
	model = Groups
