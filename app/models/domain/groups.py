from typing import List

from pydantic import Field

from .rwmodel import RWModel
from app.models.common import IDModelMixin, DateTimeModelMixin


class GroupInDB(RWModel, IDModelMixin, DateTimeModelMixin):
	name: str = Field(...)
	users: List["UserInDB"] = []
