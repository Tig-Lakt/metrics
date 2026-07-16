"""Точка сборки всех эндпоинтов версии v1.
"""

from fastapi import APIRouter

from app.api.v1.endpoints import message, process

router = APIRouter()

router.include_router(message.router)
router.include_router(process.router)
