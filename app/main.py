from contextlib import asynccontextmanager
from fastapi import FastAPI

from app.core.config import settings
from app.db.base import Base
from app.db.session import engine
from app.api.routes_auth import router as auth_router
from app.api.routes_chat import router as chat_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Управление жизненным циклом приложения: создание таблиц при старте
    """
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    await engine.dispose()


def create_app() -> FastAPI:
    """
    Фабрика приложения FastAPI
    """
    app = FastAPI(
        title=settings.APP_NAME,
        description="Защищённый API для взаимодействия с LLM через OpenRouter",
        version="1.0.0",
        lifespan=lifespan,
    )

    app.include_router(auth_router)
    app.include_router(chat_router)

    @app.get("/health", tags=["System"])
    async def health_check():
        return {"status": "ok", "environment": settings.ENVIRONMENT}

    return app

app = create_app()