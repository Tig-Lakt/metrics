"""Health-check эндпоинт.
"""

from fastapi import APIRouter, HTTPException
from sqlmodel import select

from app.db.session import DBSessionDep
from app.schemas.health import HealthStatus

# У health-check осознанно нет версионирования (/api/v1/...) — это
# инфраструктурный эндпоинт для оркестратора/балансировщика, а не часть
# публичного API, и его путь не должен меняться между версиями API.
router = APIRouter(tags=["Health"])


@router.get("/health")
async def health_check(db: DBSessionDep) -> HealthStatus:
    """Проверяет, что приложение живо и может обратиться к БД.

    Выполняет самый дешёвый возможный запрос (`SELECT 1`) через
    `session.exec()` — это метод AsyncSession из sqlmodel (не путать
    с обычным `session.execute()` из "чистого" SQLAlchemy, который
    возвращает объекты Row и требует дополнительного `.scalars()`).
    Нам не важен результат — важно лишь то, что соединение с базой
    действительно устанавливается и отвечает.
    """
    try:
        await db.exec(select(1))
    except Exception as exc:
        # 503 Service Unavailable — семантически верный код для "сервис
        # жив, но одна из его зависимостей недоступна".
        raise HTTPException(status_code=503, detail="Database unavailable") from exc

    return HealthStatus(status="healthy")
