from app.db.repositories.common import BaseCrud
from app.models.domain import ReviewInDB
from .model import Reviews


class ReviewCrud(BaseCrud[Reviews, ReviewInDB, ReviewInDB]):
	model = Reviews
