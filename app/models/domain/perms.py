from pydantic import BaseModel, Field

from app.models.common import IDModelMixin, DateTimeModelMixin
from app.models.domain.rwmodel import RWModel


class PermissionsInDB(IDModelMixin, DateTimeModelMixin, RWModel):
	code: str = Field(...)
