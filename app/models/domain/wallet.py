from __future__ import annotations
from typing import List, TYPE_CHECKING
import decimal

from pydantic import Field

from .rwmodel import RWModel
from ..common import IDModelMixin, DateTimeModelMixin

if TYPE_CHECKING:
	from .transaction import MoneyTransactionInDB


class Wallet(RWModel):
	money: decimal.Decimal
	current: str
	is_frozen: bool = False


class WalletInDB(RWModel, IDModelMixin, DateTimeModelMixin):
	money: decimal.Decimal = decimal.Decimal(0)
	current: str = Field(default="rub", max_length=4)
	transactions: List[MoneyTransactionInDB]
	is_frozen: bool = False
