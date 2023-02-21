import typing
import asyncio
import functools
from typing import Any

from app.db.engine import storage


def cache_result(
	id: str = "id",
	update_argument: str = None,
	delete: bool = False,
):
	"""
	Использвание:
	@cache_result()
	async def get(db, id: int = None):
		return await db.get(id)  # THIS RESULT WILL BE CACHED

	Примечание что бы он работал нужен что бы название
	primary key был указан явно в первом аргументе функции,
	или соответствовал "id"

	@cache_result(update_argument="value")
	async def update(db, id: int = None, value):
		x = db.update(id, value, return=True)
		return x

	Если update_argument not None or delete = True
	то тогда при вызове функции с таким же айди
	то он будет удалять эту запись из кеша.

	:param ids:
	:return:
	"""

	def wrapper(func):
		"""
		OMG TRIPLE WRAPPING!!!!

		:param func:
		:return:
		"""

		@functools.wraps(func)
		async def inner(*args, **kwargs) -> Any:
			key = str(kwargs.get(id))
			if cached_val := await storage.get(key) and not update_argument or delete:
				return cached_val
			if asyncio.iscoroutinefunction(func):
				result = await func(*args, **kwargs)
			else:
				result = func(*args, **kwargs)
			if delete:
				await storage.delete(key)
				return result
			if update_argument is not None:
				upd_val = kwargs.get(update_argument)
				await storage.set(key, upd_val)
			else:
				await storage.set(key, result)
			return result

		return inner

	return wrapper
