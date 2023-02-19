from typing import AsyncGenerator

from fastapi import Request
from sqlalchemy.ext.asyncio import AsyncSession


async def get_connection(request: Request) -> AsyncGenerator[AsyncSession, None]:
	async with request.app.state.session() as ses:
		async with ses.begin():
			yield ses
