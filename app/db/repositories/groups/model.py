import sqlalchemy as sa
from sqlalchemy.orm import relationship

from app.db.repositories.base import BaseModel
from app.db.repositories.helpers import UserToGroups


class Groups(BaseModel):
	__tablename__ = "groups"

	permissions = relationship("Permissions", uselist=False, back_populates="groups")
	name = sa.Column(sa.String(125), unique=True, primary_key=True, nullable=False)
	users = relationship("Users", back_populates="groups", secondary=UserToGroups)
