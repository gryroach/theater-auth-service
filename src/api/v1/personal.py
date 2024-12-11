from fastapi import APIRouter, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from db.db import get_session
from dependencies.auth import get_current_user
from schemas.login_history import LoginHistoryInDB, LoginRequest, LoginResponse
from schemas.user import UserCredentialsUpdate, UserData, UserInDB
from services.auth import AuthService, get_auth_service
from services.login_history import (
    LoginHistoryService,
    get_login_history_service,
)
from services.session_service import SessionService, get_session_service
from services.user import UserService, get_user_service

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
        db, user_id=str(current_user.id)
    )
    return history


@router.post(
    "/logout-all",
    status_code=status.HTTP_200_OK,
    description="Выход из всех устройств",
    summary="Выход из всех устройств",
)
async def logout_all_devices(
    current_user=Depends(get_current_user),
    session_service: SessionService = Depends(get_session_service),
) -> dict:
    """
    Выход из всех устройств с текущей сессией без ввода логина и пароля.
    """
    await session_service.increment_session_version(str(current_user.id))

    return {
        "message": "Successfully logged out from the current session.",
        "user_id": current_user.id,
    }


@router.patch(
    "/change-credentials",
    response_model=UserInDB,
    status_code=status.HTTP_200_OK,
    summary="Изменение логина и пароля пользователя",
    description=(
        "Изменение логина и пароля пользователя. "
        "После изменения происходит выход из всех устройств."
    ),
)
async def update_credentials(
    user_credentials: UserCredentialsUpdate,
    user_service: UserService = Depends(get_user_service),
    current_user: UserInDB = Depends(get_current_user),
    db: AsyncSession = Depends(get_session),
    session_service: SessionService = Depends(get_session_service),
) -> UserInDB:
    user = await user_service.update_credentials(
        db,
        current_user.id,
        user_credentials,
    )
    await session_service.increment_session_version(str(current_user.id))
    return user


@router.patch(
    "/change-user-data",
    response_model=UserInDB,
    status_code=status.HTTP_200_OK,
    description="Изменение пользовательских данных",
    summary="Изменение пользовательских данных",
)
async def update_user_data(
    user_data: UserData,
    user_service: UserService = Depends(get_user_service),
    current_user: UserInDB = Depends(get_current_user),
    db: AsyncSession = Depends(get_session),
) -> UserData:
    user = await user_service.update_credentials(
        db,
        current_user.id,
        user_data,
    )
    return user
