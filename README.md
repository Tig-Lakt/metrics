# FastAPI Observability Project

Система мониторинга и анализа производительности для FastAPI приложения с использованием Prometheus, Grafana, Loki и PostgreSQL.

## 🚀 Стек технологий
* **Backend:** FastAPI, SQLModel (async, asyncpg), Prometheus-FastAPI-Instrumentator, structlog.
* **Monitoring:** Prometheus (метрики), Grafana (визуализация).
* **Logging:** Grafana Loki + Grafana Alloy.
* **Infrastructure:** Docker, Docker Compose, Node Exporter.

## 📊 Мониторинг и Анализ (Bottleneck)
В ходе тестирования был обнаружен и зафиксирован "узкий узел" (bottleneck):
* **Эндпоинт:** `/api/v1/process`
* **Проблема:** Среднее время ответа (Latency) составляет **0.7s**, что значительно выше остальных ручек.
* **Диагностика:** Анализ панели "Latency" в Grafana показал стабильную задержку. Системные метрики (CPU/RAM) при этом остаются в норме, что подтверждает программную природу задержки (искусственный `sleep`).

## 🗂 Структура проекта
```
app/
  core/       — настройки (pydantic-settings), логирование, обработчики ошибок
  db/         — модель БД (SQLModel) и асинхронная сессия
  schemas/    — Pydantic-схемы запросов/ответов API
  api/
    health.py       — health-check (без версии — инфраструктурный эндпоинт)
    v1/
      router.py      — сборка всех роутеров v1
      endpoints/      — сами эндпоинты (message, process)
main.py       — точка входа, фабрика приложения
seed.py       — идемпотентное наполнение БД тестовыми данными
observability/ — конфиги Prometheus / Alertmanager / Grafana Alloy
tests/        — тесты на изолированной SQLite-БД (без зависимости от Postgres)
```

## 🛠 Установка и запуск
1. Клонируйте репозиторий, скопируйте `.env.example` в `.env` и заполните значения.
2. Запустите инфраструктуру:
   ```bash
   docker-compose up -d --build
   ```
3. Таблицы и тестовые данные создаются автоматически при старте приложения (см. `lifespan` в `main.py`).

### Локальный запуск без Docker
```bash
pip install .
fastapi dev main.py
```

## 🔍 Доступные эндпоинты
**Приложение:** http://localhost:8000
**Health-check:** http://localhost:8000/health
**Метрики:** http://localhost:8000/metrics
**Grafana:** http://localhost:3000 (Логин/Пароль в `.env`)
**Документация (Swagger):** http://localhost:8000/docs

## 📈 Описание Дашборда
Дашборд в Grafana включает 6 панелей:
**RPS:** Интенсивность запросов.
**Latency:** Время ответа (анализ bottleneck).
**Errors:** Мониторинг 500 ошибок (через Loki).
**CPU:** Нагрузка на процессор.
**RAM:** Нагрузка на оперативную память.
**Disk:** Свободное место на диске.

---

### Тесты
Тесты используют изолированную in-memory SQLite-базу через override
зависимости `get_db` — реальный Postgres для запуска тестов не требуется.

```bash
pip install ".[test]"
python -m pytest tests/ -v
```
