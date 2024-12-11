from fastapi import APIRouter

from .inspection import router as inspect_router
from .personal import router as login_router
from .user import router as user_router

api_router = APIRouter()
api_router.include_router(
    inspect_router,
    prefix="/inspect",
    tags=["Проверка сервисов"],
)
api_router.include_router(
    user_router,
    prefix="/users",
    tags=["API для управления пользователями"],
)
api_router.include_router(
    login_router,
    prefix="/personal",
    tags=["API личного кабинета"],
)
