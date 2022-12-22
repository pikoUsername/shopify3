from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from sentry_sdk.integrations.asgi import SentryAsgiMiddleware

from app.core.config import get_app_settings


def setup(app: FastAPI) -> None:
	settings = get_app_settings()

	if not settings.debug:
		app.add_middleware(
			SentryAsgiMiddleware,
		)
	app.add_middleware(
		CORSMiddleware,
		allow_origins=settings.allowed_hosts,
		allow_credentials=True,
		allow_methods=["*"],
		allow_headers=["*"],
	)
