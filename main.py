"""Точка входа FastAPI-приложения.

Как запускать:
    Локально (с автоперезагрузкой):   fastapi dev main.py
    В проде:                          fastapi run main.py
"""

from contextlib import asynccontextmanager

from fastapi import FastAPI
from prometheus_fastapi_instrumentator import Instrumentator

from app.api import health
from app.api.v1.router import router as v1_router
from app.core.config import settings
from app.core.exceptions import unhandled_exception_handler
from app.db.session import init_db
from seed import seed_data


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Код, который выполняется при старте и остановке приложения.

    Всё, что до `yield`, — это запуск (создать таблицы, засеять тестовые
    данные).
    """
    await init_db()
    await seed_data()
    yield


def create_app() -> FastAPI:
    """Фабрика приложения.

    Обёртка в функцию (а не просто `app = FastAPI()` на уровне модуля)
    — удобный паттерн, если понадобится создавать несколько экземпляров
    приложения (например, отдельный экземпляр для тестов с другими
    настройками).
    """
    app = FastAPI(title=settings.APP_TITLE, lifespan=lifespan)

    # /metrics — эндпоинт, который будет скрейпить Prometheus
    # (см. observability/prometheus.yml).
    Instrumentator().instrument(app).expose(app, endpoint="/metrics")

    # Единый обработчик непредвиденных ошибок вместо try/except
    # в каждом эндпоинте (см. app/core/exceptions.py).
    app.add_exception_handler(Exception, unhandled_exception_handler)

    app.include_router(health.router)
    app.include_router(v1_router)

    return app


app = create_app()
