from app.models.domain.product_lists import ProductListInDB
from ..common import BaseCrud

from .model import ProductLists


class ProductListCrud(BaseCrud[ProductLists, ProductListInDB, ProductListInDB]):
	pass
