from fastapi import FastAPI
from loguru import logger
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import create_async_engine

from app.core.settings.app import AppSettings
from app.db.engine import Session, Meta, current_session, storage


async def connect_to_db(app: FastAPI, settings: AppSettings) -> None:
	logger.info("Connecting to PostgreSQL")

	engine = create_async_engine(settings.database_url)
	Session.configure(bind=engine)
	current_session.configure(bind=engine)
	async with engine.begin() as conn:
		await conn.run_sync(Meta.create_all)

	app.state.engine = engine
	app.state.session = Session

	logger.info("Connection established")


async def connect_to_redis(app: FastAPI, settings: AppSettings) -> None:
	logger.info("Connecting to Redis")

	conn = Redis(password=settings.redis_password.get_secret_value())

	await storage.init(conn)
	app.state.storage = storage

	logger.info("Connection Established")


async def close_redis(app: FastAPI) -> None:
	await app.state.storage.close()
	logger.info("Redis connection closed")


async def close_db_connection(app: FastAPI) -> None:
	logger.info("Closing connection to database")

	app.state.session.close_all()  # note: dont add up await expr
	await app.state.engine.dispose()

	logger.info("Connection closed")
