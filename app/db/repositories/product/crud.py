from app.models.schemas.product import ProductInCreate, ProductInUpdate
from ..common import BaseCrud
from .model import Products


class ProductsCRUD(BaseCrud[Products, ProductInCreate, ProductInUpdate]):
	model = Products
