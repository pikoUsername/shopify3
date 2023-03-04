import sqlalchemy as sa
from sqlalchemy.orm import relationship

from app.db.repositories.base import TimedModel


class Products(TimedModel):
	__tablename__ = "products"

	name = sa.Column(sa.String(92), nullable=False)
	seller = relationship("Seller", back_populates="products")  # many:1
	seller_id = sa.Column(sa.ForeignKey("sellers.id", ondelete="CASCADE"))
	comments = relationship("Comments", back_populates="products")  # 1:many
	tags = relationship("Tags", back_populates="products")  # 1:many
	watches = sa.Column(sa.Integer)
	description = sa.Column(sa.Text)
	text_entities = relationship("TextEntities", back_populates="products")  # 1:many for text
	is_hidden = sa.Column(sa.Boolean, default=False)
