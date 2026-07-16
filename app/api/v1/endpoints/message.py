"""Эндпоинты для работы с сообщениями.
"""

from typing import Annotated

from fastapi import APIRouter, HTTPException, Path

from app.core.logging import logger
from app.db.models import Message
from app.db.session import DBSessionDep
from app.schemas.message import MessageRead

router = APIRouter(prefix="/api/v1/messages", tags=["Messages"])


@router.get("/{message_id}")
async def get_message(
    message_id: Annotated[int, Path(ge=1, description="ID сообщения")],
    db: DBSessionDep,
) -> MessageRead:
    """Возвращает сообщение по его ID.

    Args:
        message_id: положительный идентификатор сообщения (валидируется
            автоматически через `Path(ge=1)` — запрос с id=0 или
            отрицательным числом даже не дойдёт до тела функции).
        db: асинхронная сессия БД (внедряется через Depends).

    Raises:
        HTTPException 404: если сообщение с таким ID не найдено.
    """
    # AsyncSession.get() — самый быстрый способ получить строку по
    # первичному ключу, без необходимости писать select(Message)....
    message = await db.get(Message, message_id)

    if message is None:
        logger.warning("message_not_found", message_id=message_id)
        raise HTTPException(status_code=404, detail="Message not found")

    return MessageRead(id=message.id, text=message.text)
