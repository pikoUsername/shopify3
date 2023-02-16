import sqlalchemy as sa
from sqlalchemy.orm import relationship

from app.db.repositories.base import TimedModel
from app.db.repositories.helpers import ListsToProducts


class ProductLists(TimedModel):
	__tablename__ = 'product_lists'

	name = sa.Column(sa.String(52))
	products = relationship("Products", secondary=ListsToProducts, back_populates="product_lists")  # many:many
