import sqlalchemy as sa

from app.db.repositories.helpers import CommentSection


class Comments(CommentSection):
	__tablename__ = "comments"

	is_hidden = sa.Column(sa.Boolean, default=False)
