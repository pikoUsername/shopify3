import sqlalchemy as sa
from sqlalchemy.orm import relationship

from app.db.repositories.base import TimedModel


class Seller(TimedModel):
	"""
	Seller is linked to user model by one by one relationship
	"""
	__tablename__ = 'sellers'

	rating = sa.Column(sa.Float)  # 5 to 1
	products = relationship("Products", back_populates="products")  # M:1
	country = sa.Column(sa.String(125))
	bio = sa.Column(sa.Text)
	is_activated = sa.Column(sa.Boolean, default=True)
	is_blocked = sa.Column(sa.Boolean, default=False)

