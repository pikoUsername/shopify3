from app.models.domain.products import ProductInDB
from ..common import BaseCrud
from .model import Products


class ProductsCRUD(BaseCrud[Products, ProductInDB, ProductInDB]):
	model = Products
