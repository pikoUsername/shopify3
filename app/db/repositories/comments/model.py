import sqlalchemy as sa
from sqlalchemy.orm import relationship

from app.db.repositories.helpers import CommentSection


class Comments(CommentSection):
	__tablename__ = "comments"
