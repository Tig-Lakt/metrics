"""ORM-модели базы данных.

Почему SQLModel, а не "чистый" SQLAlchemy Base:

    Здесь она используется только как таблица; отдельные Pydantic-схемы
    для API лежат в app/schemas — так мы не отдаём наружу структуру
    таблицы напрямую (см. app/schemas/message.py).
"""

from sqlmodel import Field, SQLModel


class Message(SQLModel, table=True):
    """Таблица `messages`.

    table=True говорит SQLModel, что это не просто Pydantic-схема,
    а реальная таблица в базе данных.
    """

    __tablename__ = "messages"

    id: int | None = Field(default=None, primary_key=True)
    text: str
