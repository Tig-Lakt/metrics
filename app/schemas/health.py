"""Схема ответа для health-check эндпоинта."""

from pydantic import BaseModel


class HealthStatus(BaseModel):
    """Результат проверки состояния сервиса."""

    status: str
