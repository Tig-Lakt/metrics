"""Глобальные обработчики исключений.

Почему это лучше, чем try/except в каждом эндпоинте:

    FastAPI умеет централизованно перехватывать
    исключения через exception_handler — пишем обработку ошибок один раз,
    а не в каждом файле endpoints/*.py.

    HTTPException (404, 400 и т.д.), которые мы поднимаем сами внутри
    эндпоинтов, FastAPI обрабатывает автоматически "из коробки" — их не
    нужно перехватывать вручную. Обработчик ниже нужен только для
    ДЕЙСТВИТЕЛЬНО неожиданных ошибок (баг, недоступна БД и т.п.), чтобы
    клиент не увидел голый traceback, а получил аккуратный JSON 500.
"""

from fastapi import Request
from fastapi.responses import JSONResponse

from app.core.logging import logger


async def unhandled_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """Перехватывает любое необработанное исключение на уровне приложения.

    Args:
        request: запрос, во время обработки которого произошла ошибка.
        exc: само исключение.

    Returns:
        JSON-ответ со статусом 500, без деталей внутренней ошибки
        (детали уходят в лог, а не клиенту — иначе можно случайно
        раскрыть внутреннее устройство системы).
    """
    logger.error(
        "unhandled_exception",
        path=request.url.path,
        method=request.method,
        error=str(exc),
        exc_info=True,
    )
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal Server Error"},
    )
