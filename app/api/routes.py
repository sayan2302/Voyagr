from fastapi import APIRouter

from app.config import get_settings
from app.core import AppException

router = APIRouter()


@router.get("/health")
async def health_check() -> dict[str, str]:
    settings = get_settings()
    return {
        "status": "ok",
        "service": settings.app_name,
        "environment": settings.app_env,
    }


@router.get("/error-test")
async def error_test() -> None:
    raise AppException(message="This is a controlled test error.")
