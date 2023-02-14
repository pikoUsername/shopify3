import sqlalchemy as sa
from sqlalchemy.orm import relationship

from app.db.repositories.base import TimedModel


class Tags(TimedModel):
	__tablename__ = "tags"

	name = sa.Column(sa.String(72))
	short_description = sa.Column(sa.String(100))
	sub_tags = relationship("Tags")
	parent_tag_id = sa.Column(sa.Integer, sa.ForeignKey('tags.id'))
