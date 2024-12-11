from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from db.db import get_session
from exceptions.user_exceptions import UserDoesNotExistsError
from schemas.base import ErrorResponse
from schemas.role import Role, UpdateRole
from schemas.user import UserCreate, UserInDB
from services.user import UserService, get_user_service

router = APIRouter()


@router.post(
    "/signup",
    response_model=UserInDB,
    status_code=status.HTTP_201_CREATED,
    description="Регистрация пользователя",
    summary="Регистрация пользователя",
)
async def create_user(
    user_create: UserCreate,
    user_service: UserService = Depends(get_user_service),
    db: AsyncSession = Depends(get_session),
) -> UserInDB:
    """Регистрация пользователя."""
    user = await user_service.register_user(db, user_create)
    return user


@router.get(
    "/{user_id}/role",
    response_model=Role,
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_404_NOT_FOUND: {
            "model": ErrorResponse,
            "description": "User not found",
        }
    },
)
async def get_user_role(
    user_id: UUID,
    user_service: UserService = Depends(get_user_service),
    db: AsyncSession = Depends(get_session),
) -> Role:
    try:
        role = await user_service.get_user_role(db, user_id)
    except UserDoesNotExistsError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=e.message,
        )
    return role


@router.patch(
    "/{user_id}/role",
    response_model=Role,
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_404_NOT_FOUND: {
            "model": ErrorResponse,
            "description": "User not found",
        }
    },
)
async def set_user_role(
    user_id: UUID,
    role: UpdateRole,
    user_service: UserService = Depends(get_user_service),
    db: AsyncSession = Depends(get_session),
) -> Role:
    try:
        role = await user_service.update_role(db, user_id, role)
    except UserDoesNotExistsError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=e.message,
        )
    return role
