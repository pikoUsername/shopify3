import sqlalchemy as sa

from app.db.repositories.base import TimedModel


class MoneyTransaction(TimedModel):
	__tablename__ = 'money_transactions'

	money_change = sa.Column(sa.DECIMAL)
	approved = sa.Column(sa.Boolean, default=False)
	wallet_id = sa.Column(sa.Integer, sa.ForeignKey("wallets.id"))
