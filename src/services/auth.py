from datetime import timedelta

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.config import settings
from exceptions.auth_exceptions import (
    InvalidCredentialsError,
    InvalidSessionError,
)
from repositories.user import UserRepository
from schemas.login_history import LoginHistoryCreate
from services.jwt_service import JWTService, get_jwt_service
from services.login_history import (
    LoginHistoryService,
    get_login_history_service,
)
from services.token_service import TokenService, get_token_service


class AuthService:
    def __init__(
        self,
        user_repo: UserRepository,
        history_service: LoginHistoryService,
        token_service: TokenService,
        jwt_service: JWTService,
    ):
        self.user_repo = user_repo
        self.history_service = history_service
        self.token_service = token_service
        self.jwt_service = jwt_service
        self.access_ttl = timedelta(days=settings.ACCESS_TOKEN_EXPIRE_DAYS)
        self.refresh_ttl = timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)

    async def authenticate_user(
        self, db: AsyncSession, login: str, password: str
    ):
        user = await self.user_repo.get_by_field(db, "login", login)
        if not user or not user.check_password(password):
            raise InvalidCredentialsError()
        return user

    async def login(
        self,
        db: AsyncSession,
        login: str,
        password: str,
        ip_address: str,
        user_agent: str,
    ):
        user = await self.authenticate_user(db, login, password)
        session_version = await self.token_service.get_session_version(
            str(user.id)
        )
        if not session_version:
            session_version = 1
            await self.token_service.set_session_version(
                str(user.id), session_version
            )
        access_token = self.jwt_service.create_access_token(
            user_id=str(user.id),
            session_version=session_version,
        )
        refresh_token = self.jwt_service.create_refresh_token(
            user_id=str(user.id),
            session_version=session_version,
        )

        await self.history_service.log_login(
            db,
            LoginHistoryCreate(
                user_id=str(user.id),
                ip_address=ip_address,
                user_agent=user_agent,
            ),
        )
        return {"access_token": access_token, "refresh_token": refresh_token}

    async def logout(self, user_id: str, refresh_token: str):
        if await self.token_service.is_refresh_token_invalid(refresh_token):
            raise InvalidSessionError("This refresh token is invalid.")
        decoded = self.jwt_service.validate_token_type(
            refresh_token, "refresh"
        )
        self.jwt_service.validate_user_and_version(
            refresh_token, user_id, decoded["session_version"]
        )
        ttl = int(self.refresh_ttl.total_seconds())
        await self.token_service.logout(refresh_token, ttl)

    async def logout_all(self, user_id: str):
        await self.token_service.logout_all(user_id)

    async def refresh_tokens(self, refresh_token: str) -> dict:
        if await self.token_service.is_refresh_token_invalid(refresh_token):
            raise InvalidSessionError("This refresh token is invalid.")
        decoded = self.jwt_service.validate_token_type(
            refresh_token, "refresh"
        )
        user_id = decoded["user"]
        session_version = decoded["session_version"]
        current_version = await self.token_service.get_session_version(user_id)

        if current_version != session_version:
            raise InvalidSessionError("Session version mismatch.")

        ttl = int(self.refresh_ttl.total_seconds())
        await self.token_service.invalidate_refresh_token(refresh_token, ttl)
        return {
            "access_token": self.jwt_service.create_access_token(
                user_id, current_version
            ),
            "refresh_token": self.jwt_service.create_refresh_token(
                user_id, current_version
            ),
        }


async def get_auth_service(
    token_service: TokenService = Depends(get_token_service),
    jwt_service: JWTService = Depends(get_jwt_service),
    login_history_service: LoginHistoryService = Depends(
        get_login_history_service
    ),
) -> AuthService:
    user_repo = UserRepository()
    return AuthService(
        user_repo=user_repo,
        history_service=login_history_service,
        token_service=token_service,
        jwt_service=jwt_service,
    )
