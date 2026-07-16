"""Схемы для эндпоинта обработки данных.

Почему нужна схема запроса:

    Pydantic-модель делает эту проверку декларативно и автоматически 
    возвращает клиенту понятную ошибку 422 с указанием, какое поле не 
    так — без единой строчки кода с нашей стороны.
"""

from pydantic import BaseModel, Field


class ProcessRequest(BaseModel):
    """Тело запроса POST /api/v1/process."""

    data: str = Field(
        min_length=1,
        description="Данные для обработки. Не может быть пустой строкой.",
        examples=["some payload to process"],
    )


class ProcessResponse(BaseModel):
    """Ответ эндпоинта обработки."""

    echo: str
