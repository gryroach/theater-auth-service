from fastapi import APIRouter, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from db.db import get_session
from dependencies.auth import get_current_user
from schemas.login_history import LoginHistoryInDB, LoginRequest, LoginResponse
from schemas.refresh import TokenRefreshRequest, TokenResponse
from schemas.user import UserInDB
from services.auth import AuthService, get_auth_service
from services.login_history import (
    LoginHistoryService,
    get_login_history_service,
)

router = APIRouter()


@router.post(
    "/login",
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
        db=db, user_id=current_user.id
    )
    return history


@router.post(
    "/logout",
    status_code=status.HTTP_200_OK,
    description="Выход из текущей сессии",
    summary="Выход из текущей сессии",
)
async def logout(
    logout_token_request: TokenRefreshRequest,
    auth_service: AuthService = Depends(get_auth_service),
) -> dict:
    """
    Выход из текущей сессии. Инвалидация токена.
    """
    await auth_service.logout(
        refresh_token=logout_token_request.refresh_token,
    )
    return {"message": "Successfully logged out from the current session."}


@router.post(
    "/refresh",
    response_model=TokenResponse,
    status_code=status.HTTP_200_OK,
    description="Обновление токенов",
    summary="Обновление токенов",
)
async def refresh_tokens(
    refresh_request: TokenRefreshRequest,
    auth_service: AuthService = Depends(get_auth_service),
) -> TokenResponse:
    """
    Обновляет Access-токен с использованием валидного Refresh-токена.
    """
    new_tokens = await auth_service.refresh_tokens(
        refresh_token=refresh_request.refresh_token
    )
    return new_tokens


@router.post(
    "/logout/all",
    status_code=status.HTTP_200_OK,
    description="Выход из всех устройств",
    summary="Выход из всех устройств",
)
async def logout_all_devices(
    current_user: UserInDB = Depends(get_current_user),
    auth_service: AuthService = Depends(get_auth_service),
) -> dict:
    """
    Выход из всех устройств, инвалидация всех токенов пользователя.
    """
    await auth_service.logout_all(user_id=str(current_user.id))
    return {
        "message": "Successfully logged out from all devices.",
        "user_id": current_user.id,
    }