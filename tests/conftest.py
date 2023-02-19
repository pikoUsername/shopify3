from os import environ

import pytest
from asgi_lifespan import LifespanManager
from fastapi import FastAPI
from httpx import AsyncClient

from sqlalchemy.ext.asyncio import AsyncSession

from app.db.repositories.user import UserCrud, Users
from app.models.domain.users import UserInDB
from app.models.schemas.users import UserInCreate
from app.services import jwt

environ["APP_ENV"] = "test"


@pytest.fixture
def app() -> FastAPI:
    from app.main import get_application  # local import for testing purpose

    return get_application()


@pytest.fixture
async def initialized_app(app: FastAPI) -> FastAPI:
    async with LifespanManager(app):
        return app


@pytest.fixture
def db(initialized_app: FastAPI) -> AsyncSession:
    async with initialized_app.state.session() as ses:
        async with ses.begin():
            return ses


@pytest.fixture
async def client(initialized_app: FastAPI) -> AsyncClient:
    async with AsyncClient(
        app=initialized_app,
        base_url="http://testserver",
        headers={"Content-Type": "application/json"},
    ) as client:
        yield client


@pytest.fixture
def authorization_prefix() -> str:
    from app.core.config import get_app_settings

    settings = get_app_settings()
    jwt_token_prefix = settings.jwt_token_prefix

    return jwt_token_prefix


@pytest.fixture
def test_user_schema() -> UserInDB:
    return UserInDB(
        username="TestUser",
        email="TestUser",
    )


@pytest.fixture
async def test_user(db: AsyncSession, test_user_schema: UserInDB) -> Users:
    test_user_schema = UserInCreate(
        username=test_user_schema.username,
        email=test_user_schema.email,
        passowrd="Test@password"
    )

    return await UserCrud.create(db, test_user_schema)


@pytest.fixture
def token(test_user: UserInDB) -> str:
    return jwt.create_access_token_for_user(test_user, environ["SECRET_KEY"])


@pytest.fixture
def authorized_client(
    client: AsyncClient, token: str, authorization_prefix: str
) -> AsyncClient:
    client.headers = {
        "Authorization": f"{authorization_prefix} {token}",
        **client.headers,
    }
    return client
