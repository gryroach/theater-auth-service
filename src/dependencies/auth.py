import jwt
from fastapi import Depends, Request
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession

from db.db import get_session
from exceptions.auth_exceptions import (
    InvalidAuthenticationScheme,
    InvalidTokenError,
    TokenExpiredError,
)
from exceptions.user_exceptions import UserNotFoundError
from schemas.entity import UserInDB
from services.jwt_service import JWTService, get_jwt_service
from services.user import UserService, get_user_service


class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super().__init__(auto_error=auto_error)

    async def __call__(self, request: Request) -> HTTPAuthorizationCredentials:
        credentials: HTTPAuthorizationCredentials = await super().__call__(
            request
        )
        if credentials and credentials.scheme == "Bearer":
            return credentials.credentials
        raise InvalidAuthenticationScheme("Invalid authentication scheme.")


async def get_current_user(
    token: str = Depends(JWTBearer()),
    jwt_service: JWTService = Depends(get_jwt_service),
    user_service: UserService = Depends(get_user_service),
    db: AsyncSession = Depends(get_session),
) -> UserInDB:
    try:
        payload = jwt_service.decode_token(token)
        user_id = payload.get("user")
        session_version = payload.get("session_version")
    except jwt.ExpiredSignatureError:
        raise TokenExpiredError("Token expired")
    except jwt.InvalidTokenError:
        raise InvalidTokenError("Invalid token")

    current_version = await user_service.token_service.get_session_version(
        user_id
    )
    if not current_version or int(current_version) != int(session_version):
        raise InvalidTokenError("Session is invalid or expired")

    user = await user_service.user_repo.get(db, user_id)
    if not user:
        raise UserNotFoundError("User not found")
    return user
