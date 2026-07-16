"""Эндпоинт "обработки" данных (имитация тяжёлой операции).
"""

import asyncio

from fastapi import APIRouter

from app.core.logging import logger
from app.schemas.process import ProcessRequest, ProcessResponse

router = APIRouter(prefix="/api/v1/process", tags=["Process"])


@router.post("")
async def process_data(payload: ProcessRequest) -> ProcessResponse:
    """Имитирует обработку данных с задержкой и возвращает эхо-ответ.

    `asyncio.sleep` здесь — честная асинхронная задержка (заглушка
    вместо реальной тяжёлой работы, например вызова внешнего API).
    Именно поэтому эта функция обоснованно `async def`: она ждёт
    (`await`), а не блокирует поток.
    """
    await asyncio.sleep(0.7)

    logger.info("data_processed", input_length=len(payload.data))

    return ProcessResponse(echo=payload.data)
