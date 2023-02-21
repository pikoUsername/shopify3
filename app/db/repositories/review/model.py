import sqlalchemy as sa

from app.db.repositories.helpers import CommentSection


class Reviews(CommentSection):
	"""
	For anything that has rating column
	"""
	__tablename__ = "reviews"

	rating = sa.Column(sa.Integer)
