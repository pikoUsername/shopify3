from typing import TYPE_CHECKING

import sqlalchemy as sa
from sqlalchemy.orm import relationship, mapped_column, Mapped

from app.db.repositories.base import TimedModel

if TYPE_CHECKING:
	from app.db.repositories.wallet import Wallet


class MoneyTransaction(TimedModel):
	__tablename__ = 'money_transactions'

	money_change: Mapped[sa.DECIMAL] = mapped_column(sa.DECIMAL)
	approved: Mapped[bool] = mapped_column(default=False)
	wallet_id: Mapped[int] = mapped_column(sa.ForeignKey("wallets.id"))
	wallet: Mapped["Wallet"] = relationship(back_populates="transactions")  # M:1
