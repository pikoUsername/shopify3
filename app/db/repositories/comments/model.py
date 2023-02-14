import sqlalchemy as sa
from sqlalchemy.orm import relationship

from app.db.repositories.base import TimedModel


class Comments(TimedModel):
	__tablename__ = "comments"

	author = relationship("Users", back_populates="comments")
	author_id = sa.Column(sa.ForeignKey("users.id", ondelete="SET NULL"))
	content = sa.Column(sa.String(256), nullable=False)
	text_entities = relationship("TextItems", back_populates="comments")
