from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parent.parent

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_prefix="",
        case_sensitive=False,
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # Общие настройки
    APP_NAME: str = "LLM API"
    ENVIRONMENT: str = "development"
    DEBUG: bool = True

    # JWT
    JWT_SECRET: str
    JWT_ALGORITHM: str = "HS256"
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # База данных (SQLite)
    SQLITE_PATH: str = str(BASE_DIR / "app.db")

    # OpenRouter
    OPENROUTER_API_KEY: str
    OPENROUTER_BASE_URL: str = "https://openrouter.ai/api/v1"
    OPENROUTER_DEFAULT_MODEL: str = "openrouter/free"
    OPENROUTER_REFERER: str | None = "http://localhost:8000"
    OPENROUTER_TITLE: str | None = "My LLM App"
    OPENROUTER_TIMEOUT: float = 60.0

settings = Settings()