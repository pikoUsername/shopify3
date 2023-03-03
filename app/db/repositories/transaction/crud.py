from sqlalchemy.ext.asyncio import AsyncSession

from app.models.domain import MoneyTransactionInDB
from ..common import BaseCrud

from .model import MoneyTransaction


class TransactionCRUD(
	BaseCrud[MoneyTransaction, MoneyTransactionInDB, MoneyTransactionInDB]
):
	model = MoneyTransaction

	@classmethod
	async def create(
		cls, db: AsyncSession, obj_in: MoneyTransactionInDB
	) -> MoneyTransaction:
		return await super().create(db, obj_in)
