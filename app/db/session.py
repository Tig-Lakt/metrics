"""Подключение к БД и dependency для получения сессии в эндпоинтах.
"""

from collections.abc import AsyncIterator
from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlmodel import SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession

from app.core.config import settings

# echo=False — не логировать каждый SQL-запрос в stdout (включи True для
# локального дебага, если нужно увидеть сырые SQL-запросы).
# pool_pre_ping=True — перед использованием соединения из пула SQLAlchemy
# "пингует" его; без этого можно словить обрыв соединения после того,
# как Postgres или сеть немного "полежали" (частый кейс в контейнерах).
engine = create_async_engine(settings.database_url, echo=False, pool_pre_ping=True)

# async_sessionmaker — фабрика сессий. class_=AsyncSession (из sqlmodel,
# не из "чистого" sqlalchemy!) даёт нам метод .exec(select(...)), который
# удобнее, чем связка .execute(...).scalars().
AsyncSessionLocal = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


async def get_db() -> AsyncIterator[AsyncSession]:
    """Dependency FastAPI: выдаёт сессию БД на время обработки запроса.

    Паттерн "yield" гарантирует, что сессия закроется (в блоке after yield,
    выполняемом FastAPI автоматически) даже если внутри эндпоинта
    вылетело исключение — аналог try/finally, но силами самого FastAPI.
    """
    async with AsyncSessionLocal() as session:
        yield session


# Type alias для dependency injection в стиле Annotated. 
DBSessionDep = Annotated[AsyncSession, Depends(get_db)]


async def init_db() -> None:
    """Создаёт таблицы в БД, если их ещё нет.

    Вызывается один раз при старте приложения (см. lifespan в main.py).
    Для реального прод-проекта это обычно заменяют на Alembic-миграции —
    но для небольшого сервиса мониторинга create_all — осознанно
    достаточное решение.
    """
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)
