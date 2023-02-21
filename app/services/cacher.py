import abc
import asyncio
import functools
from typing import Any, Tuple, Optional

from redis.asyncio import Redis


class CacheInterface(abc.ABC):
	@abc.abstractmethod
	async def get(self, key: str) -> Any:
		pass

	@abc.abstractmethod
	async def set(self, key: str, value: Any) -> Any:
		pass

	@abc.abstractmethod
	async def delete(self, key: str, return_: bool = False) -> Any:
		pass

	@abc.abstractmethod
	async def close(self) -> None:
		pass

	async def get_or_set(self, key: str, value: Any) -> Tuple[Any, bool]:
		if v := await self.get(key):
			return v, False
		return await self.set(key, value), True


class RedisCache(CacheInterface):
	def __init__(self, conn: Optional[Redis] = None, lazy: bool = False) -> None:
		if conn is None and lazy is False:
			raise ValueError("Connection argument is missing, lazy = False")
		self.conn = conn

	async def init(self, redis: Redis):
		await redis.ping()
		self.conn = redis

	async def get(self, key: str) -> Any:
		return await self.conn.get(key)

	async def set(self, key: str, value: Any) -> Any:
		return await self.conn.set(key, value)

	async def delete(self, key: str, return_: bool = False) -> Any:
		if return_:
			return await self.conn.getdel(key)
		await self.conn.delete(key)

	async def close(self) -> None:
		await super().close()

	def __getattr__(self, item: str) -> Any:
		# to let dev use cacher like this storage.hset("kkk", "1231")
		# instead of storage.conn.hset("hhh", "1231")
		# which is not so good
		if item.startswith("__") and item.endswith("__"):
			return getattr(self, item)
		if item in self.conn.__dict__ and item in self.__dict__:
			return getattr(self, item)
		if item in self.conn.__dict__:
			x = getattr(self.conn, item)
			if callable(x):
				return x
			raise ValueError("Only functions allowed to get directly")
		return getattr(self, item)
