from fastapi import APIRouter, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from db.db import get_session
from dependencies.auth import get_current_user
from schemas.entity import (
    LoginHistoryInDB,
    LoginRequest,
    LoginResponse,
    UserInDB,
)
from services.auth import AuthService, get_auth_service
from services.login_history import (
    LoginHistoryService,
    get_login_history_service,
)

router = APIRouter()


@router.post(
    "/",
    response_model=LoginResponse,
    status_code=status.HTTP_200_OK,
    description="Аутентификация пользователя",
    summary="Аутентификация пользователя",
)
async def login(
    request: Request,
    login_request: LoginRequest,
    db: AsyncSession = Depends(get_session),
    auth_service: AuthService = Depends(get_auth_service),
):
    """Аутентификация пользователя."""
    ip_address = request.client.host
    user_agent = request.headers.get("User-Agent", "")
    tokens = await auth_service.login(
        db,
        login_request.login,
        login_request.password,
        ip_address,
        user_agent,
    )
    return tokens


@router.get(
    "/login-history",
    response_model=list[LoginHistoryInDB],
    description="История входов",
    summary="История входов",
)
async def get_login_history(
    db: AsyncSession = Depends(get_session),
    current_user: UserInDB = Depends(get_current_user),
    history_service: LoginHistoryService = Depends(get_login_history_service),
):
    """Получить историю входов текущего пользователя."""
    history = await history_service.get_user_history(
        db, user_id=current_user.id
    )
    return history
