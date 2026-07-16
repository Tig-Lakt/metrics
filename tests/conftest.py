"""Общие фикстуры pytest.
"""

import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlmodel import SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession

from app.db.session import get_db
from main import app


@pytest_asyncio.fixture
async def async_client():
    """Асинхронный HTTP-клиент, работающий с приложением in-memory.

    base_url="http://test" — это условное значение, требуемое httpx для
    формирования запросов; никакого реального сетевого обращения не
    происходит, всё выполняется в процессе через ASGITransport.
    """
    test_engine = create_async_engine("sqlite+aiosqlite:///:memory:")
    test_session_factory = async_sessionmaker(
        test_engine, class_=AsyncSession, expire_on_commit=False
    )

    # Создаём схему таблиц в тестовой SQLite-базе.
    async with test_engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)

    async def _override_get_db():
        async with test_session_factory() as session:
            yield session

    # Подменяем зависимость get_db только на время теста.
    app.dependency_overrides[get_db] = _override_get_db

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        yield client

    app.dependency_overrides.clear()
    await test_engine.dispose()
