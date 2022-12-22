from fastapi import FastAPI
from loguru import logger
from sqlalchemy.ext.asyncio import create_async_engine, AsyncConnection

from app.core.settings.app import AppSettings
from app.db.engine import Session, Meta, current_session


async def connect_to_db(app: FastAPI, settings: AppSettings) -> None:
    logger.info("Connecting to PostgreSQL")

    engine = create_async_engine(settings.database_url)
    Session.configure(bind=engine)
    current_session.configure(bind=engine)
    async with engine.begin() as conn:
        conn: AsyncConnection
        await conn.run_sync(Meta.create_all)

    app.state.engine = engine
    app.state.session = Session()

    logger.info("Connection established")


async def close_db_connection(app: FastAPI) -> None:
    logger.info("Closing connection to database")

    await app.state.session.close()
    await app.state.engine.dispose()

    logger.info("Connection closed")
