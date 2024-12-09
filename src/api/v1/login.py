from fastapi import APIRouter, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from db.db import get_session
from dependencies.auth import get_current_user
from repositories.login_history import LoginHistoryRepository
from schemas.entity import (
    LoginHistoryInDB,
    LoginRequest,
    LoginResponse,
    UserInDB,
)
from services.auth import AuthService, get_auth_service

router = APIRouter()


@router.post("/", response_model=LoginResponse, status_code=status.HTTP_200_OK)
async def login(
    request: Request,
    login_request: LoginRequest,
    db: AsyncSession = Depends(get_session),
    auth_service: AuthService = Depends(get_auth_service),
):
    ip_address = request.client.host
    user_agent = request.headers.get("User-Agent", "")
    tokens = await auth_service.login(
        db,
        login_request.login,
        login_request.password,
        ip_address,
        user_agent,
        access_exp=login_request.access_exp,
        refresh_exp=login_request.refresh_exp,
    )
    return tokens


@router.get("/login-history", response_model=list[LoginHistoryInDB])
async def get_login_history(
    db: AsyncSession = Depends(get_session),
    current_user: UserInDB = Depends(get_current_user),
    history_repo: LoginHistoryRepository = Depends(),
):
    history = await history_repo.get_multi(db, skip=0, limit=100)
    return history
