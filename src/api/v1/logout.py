from fastapi import APIRouter, Depends
from starlette import status

from dependencies.auth import get_current_user
from services.token_service import TokenService, get_token_service

router = APIRouter()


@router.post(
    "/all",
    status_code=status.HTTP_200_OK,
    description="Выход из всех устройств",
    summary="Выход из всех устройств",
)
async def logout_all_devices(
    current_user=Depends(get_current_user),
    token_service: TokenService = Depends(get_token_service),
) -> dict:
    """
    Выход из всех устройств с текущей сессией без ввода логина и пароля.
    """
    await token_service.increment_session_version(str(current_user.id))

    return {
        "message": "Successfully logged out from the current session.",
        "user_id": current_user.id,
    }
