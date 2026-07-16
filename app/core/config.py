"""Конфигурация приложения."""

from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Все настройки приложения в одном месте.

    Значения по умолчанию — только там, где дефолт действительно безопасен
    (например, порт Postgres). Для секретов (пароль, логин) дефолтов нет:
    их отсутствие в .env должно приводить к ошибке запуска, а не к тихой
    работе с пустой строкой.
    """

    # model_config говорит pydantic-settings, откуда брать .env файл.
    # extra="ignore" — не падать, если в .env есть переменные, которые
    # не описаны в этом классе (например, GRAFANA_* — они нужны только
    # docker-compose, а не самому приложению).
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    APP_TITLE: str = "FastAPI Observability"

    # --- Postgres ---
    DB_HOST: str
    DB_PORT: int = 5432
    DB_NAME: str
    DB_USER: str
    DB_PASSWORD: str

    @property
    def database_url(self) -> str:
        """Собирает URL подключения к БД для асинхронного драйвера asyncpg.
        """
        return (
            f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASSWORD}"
            f"@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        )


@lru_cache
def get_settings() -> Settings:
    """Возвращает настройки, создавая их только один раз (кэш).

    lru_cache тут — простая замена "синглтону": Settings() читает .env
    и валидирует его, это недорого, но незачем делать это на каждый вызов.
    """
    return Settings()


# Готовый объект для удобного импорта: `from app.core.config import settings`
settings = get_settings()
