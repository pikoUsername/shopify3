from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession

from app.db.engine import Session


async def get_connection() -> AsyncGenerator[AsyncSession, None]:
    async with Session() as ses:
        ses: AsyncSession
        async with ses.begin():
            yield ses
