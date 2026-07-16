# Stage 1: Build
FROM python:3.11-slim as builder

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY . .
RUN pip install --no-cache-dir --prefix=/install .

# Stage 2: Runtime
FROM python:3.11-slim

WORKDIR /app

COPY --from=builder /install /usr/local
COPY . .

# Безопасность: работаем под не-privileged пользователем
RUN useradd -m appuser && chown -R appuser /app
USER appuser

EXPOSE 8000

# `fastapi run` — рекомендованный способ запуска в проде (см. main.py).

CMD ["fastapi", "run", "main.py", "--host", "0.0.0.0", "--port", "8000"]