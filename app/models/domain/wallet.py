from .rwmodel import RWModel
from ..common import IDModelMixin, DateTimeModelMixin


class WalletInDB(RWModel, IDModelMixin, DateTimeModelMixin):
	pass
