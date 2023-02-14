from pydantic import condecimal, Field

from .rwmodel import RWModel
from ..common import IDModelMixin, DateTimeModelMixin


class MoneyTransactionInDB(IDModelMixin, DateTimeModelMixin, RWModel):
	money_change: condecimal(max_digits=4)
	approved: bool = Field(default=False)
	wallet_id: int
