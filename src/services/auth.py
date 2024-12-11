from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.config import settings
from db.db import get_session
from exceptions.auth_exceptions import InvalidCredentialsError
from repositories.login_history import LoginHistoryRepository
from repositories.user import UserRepository
from schemas.login_history import LoginHistoryCreate
from services.jwt_service import JWTService, get_jwt_service
from services.session_service import SessionService, get_session_service


class AuthService:
    def __init__(
        self,
        user_repo: UserRepository,
        history_repo: LoginHistoryRepository,
        session_service: SessionService,
        jwt_service: JWTService,
    ):
        self.user_repo = user_repo
        self.history_repo = history_repo
        self.session_service = session_service
        self.jwt_service = jwt_service

    async def authenticate_user(
        self, db: AsyncSession, login: str, password: str
    ):
        user = await self.user_repo.get_by_field(db, "login", login)
        if not user or not user.check_password(password):
            raise InvalidCredentialsError("Wrong login or password")
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

        session_version = await self.session_service.get_session_version(
            str(user.id)
        )
        if not session_version:
            session_version = 1
            await self.session_service.set_session_version(
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

        await self.history_repo.create(
            db,
            obj_in=LoginHistoryCreate(
                user_id=str(user.id),
                ip_address=ip_address,
                user_agent=user_agent,
            ),
        )

        return {"access_token": access_token, "refresh_token": refresh_token}


async def get_auth_service(
    session_service: SessionService = Depends(get_session_service),
    jwt_service: JWTService = Depends(get_jwt_service),
) -> AuthService:
    user_repo = UserRepository()
    history_repo = LoginHistoryRepository()
    return AuthService(
        user_repo=user_repo,
        history_repo=history_repo,
        session_service=session_service,
        jwt_service=jwt_service,
    )
