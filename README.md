# FastAPI Observability Project

Система мониторинга и анализа производительности для FastAPI приложения с использованием Prometheus, Grafana, Loki и PostgreSQL.

## 🚀 Стек технологий
* **Backend:** FastAPI, SQLAlchemy, Prometheus-FastAPI-Instrumentator.
* **Monitoring:** Prometheus (метрики), Grafana (визуализация).
* **Logging:** Grafana Loki + Grafana Alloy.
* **Infrastructure:** Docker, Docker Compose, Node Exporter.

## 📊 Мониторинг и Анализ (Bottleneck)
В ходе тестирования был обнаружен и зафиксирован "узкий узел" (bottleneck):
* **Эндпоинт:** `/process`
* **Проблема:** Среднее время ответа (Latency) составляет **0.7s**, что значительно выше остальных ручек.
* **Диагностика:** Анализ панели "Latency" в Grafana показал стабильную задержку. Системные метрики (CPU/RAM) при этом остаются в норме, что подтверждает программную природу задержки (искусственный `sleep`).

## 🛠 Установка и запуск
1. Клонируйте репозиторий.
2. Запустите инфраструктуру:
   ```bash
   docker-compose up -d --build
3. Инициализация базы данных происходит автоматически.

## 🔍 Доступные эндпоинты  
**Приложение:** http://localhost:8000  
**Метрики:** http://localhost:8000/metrics  
**Grafana:** http://localhost:3000 (Логин/Пароль в .env)  
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

### Действия после завершения настройки базы:  
1. **Запустить тесты**:  
   ```bash
   pytest tests/test_main.py  
