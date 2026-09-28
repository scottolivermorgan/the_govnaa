from fastapi import APIRouter

from app.core.config import get_settings

router = APIRouter()


@router.get("/")
def index() -> dict[str, str]:
    return {
        "name": "Data Governor",
        "status": "running",
        "health": "/health",
    }


@router.get("/health")
def health() -> dict[str, object]:
    settings = get_settings()
    return {
        "status": "ok",
        "execution_enabled": settings.execution_enabled,
        "roots": [root.model_dump() for root in settings.roots],
    }
