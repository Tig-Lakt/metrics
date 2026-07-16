"""Наполнение БД тестовыми данными."""

import asyncio

from sqlmodel import select

from app.core.logging import logger
from app.db.models import Message
from app.db.session import AsyncSessionLocal, init_db


async def seed_data() -> None:
    """Заполняет таблицу messages тестовыми строками, если она пуста.

    Идемпотентна: повторный вызов при уже заполненной таблице ничего
    не делает — это важно, потому что функция вызывается при КАЖДОМ
    старте приложения (см. lifespan в main.py), а не только один раз.
    """
    async with AsyncSessionLocal() as session:
        existing = await session.exec(select(Message).limit(1))
        if existing.first() is not None:
            logger.info("seed_skipped", reason="database already has data")
            return

        messages = [Message(text=f"Static message number {i}") for i in range(1, 11)]
        session.add_all(messages)
        await session.commit()
        logger.info("seed_completed", count=len(messages))


async def _main() -> None:
    """Позволяет запустить сидирование отдельно: `python seed.py`."""
    await init_db()
    await seed_data()


if __name__ == "__main__":
    asyncio.run(_main())
