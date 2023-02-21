from .rwmodel import RWModel
from .base import CommentSection


class ReviewInDB(RWModel, CommentSection):
	rating: int
