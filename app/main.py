from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api import router
from app.config import get_settings
from app.core import (
    configure_logging,
    get_logger,
    register_exception_handlers,
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    configure_logging()
    settings = get_settings()
    logger = get_logger(__name__)

    logger.info("%s is starting up in %s mode...", settings.app_name, settings.app_env)
    yield
    logger.info("%s is shutting down...", settings.app_name)


def create_app() -> FastAPI:
    settings = get_settings()

    app = FastAPI(
        title=settings.app_name,
        version="0.1.0",
        debug=settings.debug,
        lifespan=lifespan,
    )

    register_exception_handlers(app)
    app.include_router(router, prefix=settings.api_v1_prefix)

    return app


app = create_app()
