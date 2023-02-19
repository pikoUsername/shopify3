import sqlalchemy as sa
from sqlalchemy.orm import relationship

from ..base import TimedModel
from ..transaction import MoneyTransaction


class Wallet(TimedModel):
	__tablename__ = "wallets"

	_money = sa.Column(sa.DECIMAL, default=0)
	current = sa.Column(sa.String(5))
	transactions = relationship("MoneyTransaction", back_populates="wallets")
	is_frozen = sa.Column(sa.Boolean, default=False)

	@property
	def money(self) -> int:
		return self._money

	@money.setter
	def money(self) -> None:
		raise ValueError("Not allowed to set money field")

	def add_money(self, money: int) -> MoneyTransaction:
		pass  # TODO
