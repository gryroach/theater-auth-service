from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from db.db import get_session
from schemas.entity import LoginRequest
from services.auth import AuthService, get_auth_service
from services.token_service import TokenService, get_token_service

router = APIRouter()


@router.post(
    "/all",
    status_code=status.HTTP_200_OK,
    summary="Выход из всех устройств",
)
async def logout_all_devices(
    login_request: LoginRequest,
    db: AsyncSession = Depends(get_session),
    auth_service: AuthService = Depends(get_auth_service),
    token_service: TokenService = Depends(get_token_service),
) -> dict:
    """
    Выход из всех устройств с проверкой логина и пароля.
    """
    user = await auth_service.authenticate_user(
        db, login_request.login, login_request.password
    )

    await token_service.increment_session_version(str(user.id))

    return {
        "message": "Successfully logged out from all devices. Tokens are now invalidated.",
        "user_id": user.id,
    }
