from app.models.domain.product_lists import ProductList
from ..common import BaseCrud

from .model import ProductLists


class ProductListCrud(BaseCrud[ProductLists, ProductList, ProductList]):
	model = ProductLists
