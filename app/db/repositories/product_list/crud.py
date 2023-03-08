from app.models.domain import ProductListInDB
from ..common import BaseCrud

from .model import ProductLists


class ProductListCrud(BaseCrud[ProductLists, ProductListInDB, ProductListInDB]):
	model = ProductLists
