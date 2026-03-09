import os
import sys

project_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_path)

import pytest
import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from main import app
from config.config import BASE_URL


@pytest_asyncio.fixture
async def async_client():
    """Фикстура создающая асинхронного клиента."""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url=BASE_URL) as ac:
        yield ac 


@pytest.mark.asyncio
async def test_health_check(async_client): 
    response = await async_client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}


@pytest.mark.asyncio
async def test_metrics_endpoint(async_client):
    response = await async_client.get("/metrics")
    assert response.status_code == 200
    # Проверка присутствия метрик
    assert "http_requests_total" in response.text
    assert "http_request_duration_seconds" in response.text


@pytest.mark.asyncio
async def test_process_bottleneck_logic(async_client):
    response = await async_client.post("/process", json={"data": "test_unit"})
    assert response.status_code == 200
    assert "echo" in response.json()