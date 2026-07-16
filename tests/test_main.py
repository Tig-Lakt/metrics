"""Тесты основных эндпоинтов.
"""

import pytest


@pytest.mark.asyncio
async def test_health_check(async_client):
    """/health должен отвечать 200 и {"status": "healthy"}, когда БД жива."""
    response = await async_client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}


@pytest.mark.asyncio
async def test_metrics_endpoint(async_client):
    """/metrics должен содержать стандартные метрики Instrumentator."""
    response = await async_client.get("/metrics")
    assert response.status_code == 200
    # Имена метрик, которые прометей-инструментатор публикует по умолчанию.
    assert "http_requests_total" in response.text
    assert "http_request_duration_seconds" in response.text


@pytest.mark.asyncio
async def test_process_returns_echo(async_client):
    """POST /api/v1/process должен вернуть переданные данные обратно."""
    response = await async_client.post("/api/v1/process", json={"data": "test_unit"})
    assert response.status_code == 200
    assert response.json() == {"echo": "test_unit"}


@pytest.mark.asyncio
async def test_process_rejects_empty_data(async_client):
    """Пустая строка `data` должна отклоняться валидацией схемы (422)."""
    response = await async_client.post("/api/v1/process", json={"data": ""})
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_get_message_not_found(async_client):
    """Несуществующее сообщение должно возвращать 404."""
    response = await async_client.get("/api/v1/messages/999")
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_get_message_success(async_client):
    """Сообщение, добавленное напрямую через БД, должно быть доступно по API."""
    from app.db.models import Message
    from app.db.session import get_db
    from main import app

    # Получаем ту же (тестовую) сессию, что и API, через override-фабрику.
    override = app.dependency_overrides[get_db]
    async for session in override():
        session.add(Message(id=1, text="hello from test"))
        await session.commit()
        break

    response = await async_client.get("/api/v1/messages/1")
    assert response.status_code == 200
    assert response.json() == {"id": 1, "text": "hello from test"}
