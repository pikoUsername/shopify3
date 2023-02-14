import asyncio
import pathlib
import sys
from logging.config import fileConfig

from dotenv import load_dotenv
from alembic import context
from sqlalchemy import pool
from sqlalchemy.ext.asyncio import async_engine_from_config

sys.path.append(str(pathlib.Path(__file__).resolve().parents[3]))

from app.db.engine import Meta
from app.db.repositories.permissions import Permissions
from app.db.repositories.user import Users
from app.db.repositories.transaction import MoneyTransaction
from app.db.repositories.seller import Seller
from app.db.repositories.wallet import Wallet
from app.db.repositories.groups import Groups
from app.core.config import get_app_settings

load_dotenv()

config = context.config

if config.config_file_name is not None:
	fileConfig(config.config_file_name)

# and using their metadata
target_metadata = Meta

postgres_url = get_app_settings().database_url
config.set_main_option("sqlalchemy.url", postgres_url)


def run_migrations_offline():
	"""Run migrations in 'offline' mode.

	This configures the context with just a URL
	and not an Engine, though an Engine is acceptable
	here as well.  By skipping the Engine creation
	we don't even need a DBAPI to be available.

	Calls to context.execute() here emit the given string to the
	script output.

	"""
	url = config.get_main_option("sqlalchemy.url")
	context.configure(
		url=url,
		target_metadata=target_metadata,
		literal_binds=True,
		dialect_opts={"paramstyle": "named"},
	)

	with context.begin_transaction():
		context.run_migrations()


def do_run_migrations(connection):
	context.configure(
		connection=connection,
		target_metadata=target_metadata,
		include_schemas=True,
	)

	with context.begin_transaction():
		context.run_migrations()


async def run_migrations_online():
	"""Run migrations in 'online' mode.

	In this scenario we need to create an Engine
	and associate a connection with the context.

	"""
	connectable = async_engine_from_config(
		config.get_section(config.config_ini_section),
		prefix="sqlalchemy.",
		poolclass=pool.NullPool,
	)

	async with connectable.connect() as connection:
		await connection.run_sync(do_run_migrations)

	await connectable.dispose()


if context.is_offline_mode():
	run_migrations_offline()
else:
	asyncio.run(run_migrations_online())
