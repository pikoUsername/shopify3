from typing import List, TYPE_CHECKING

from pydantic import Field

from .rwmodel import RWModel
from app.models.common import IDModelMixin, DateTimeModelMixin


if TYPE_CHECKING:
	from app.models.domain.users import UserInDB


class GroupInDB(RWModel, IDModelMixin, DateTimeModelMixin):
	name: str = Field(...)
	users: List["UserInDB"] = []
