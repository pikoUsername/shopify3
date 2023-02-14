from app.models.domain.seller import SellerInDB
from ..common import BaseCrud

from .model import Seller


class SellerCRUD(BaseCrud[Seller, SellerInDB, SellerInDB]):
	model = Seller
