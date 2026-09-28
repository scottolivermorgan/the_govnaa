from fastapi import FastAPI

from app.api.catalogue import router as catalogue_router
from app.api.health import router as health_router
from app.core.config import get_settings
from app.db.session import init_db


def create_app() -> FastAPI:
    settings = get_settings()
    app = FastAPI(title=settings.app_name)

    @app.on_event("startup")
    def startup() -> None:
        init_db()

    app.include_router(catalogue_router)
    app.include_router(health_router)
    return app


app = create_app()
