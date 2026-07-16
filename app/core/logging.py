"""Структурированное логирование через structlog.

Почему структурированные логи, а не print/logging с текстом:
    Логи в формате JSON легко парсит Loki/Grafana/ELK — можно фильтровать
    по полям (например message_id=42), а не грепать текст регулярками.
"""

import structlog

structlog.configure(
    processors=[
        # Добавляет уровень лога (info/warning/error) в итоговый JSON.
        structlog.processors.add_log_level,
        # Добавляет ISO-таймстамп — без него сложно сопоставлять логи
        # с метриками и трейсами по времени.
        structlog.processors.TimeStamper(fmt="iso"),
        # Если в лог передали exc_info=True — красиво форматирует traceback.
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
        # Финальный шаг — сериализация в JSON. Он должен быть последним.
        structlog.processors.JSONRenderer(),
    ],
    # Кэшируем логгер на первый вызов — чуть быстрее на горячем пути.
    cache_logger_on_first_use=True,
)

# Готовый логгер для импорта: `from app.core.logging import logger`
logger = structlog.get_logger()
