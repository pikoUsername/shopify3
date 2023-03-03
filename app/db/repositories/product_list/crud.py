from app.models.domain import ProductList
from ..common import BaseCrud

from .model import ProductLists


class ProductListCrud(BaseCrud[ProductLists, ProductList, ProductList]):
	model = ProductLists
