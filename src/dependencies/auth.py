import jwt
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from core.config import settings
from db.db import get_session
from repositories.user import UserRepository
from schemas.entity import UserInDB
from services.jwt_service import JWTService, get_jwt_service
from services.token_service import TokenService, get_token_service

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_session),
    jwt_service: JWTService = Depends(get_jwt_service),
    token_service: TokenService = Depends(get_token_service),
) -> UserInDB:
    try:
        payload = jwt_service.decode_token(token)
        user_id = payload.get("user")
        session_version = payload.get("session_version")
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token expired",
        )
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
        )

    current_version = await token_service.get_session_version(user_id)
    if current_version is None or int(current_version) != int(session_version):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Session is invalid or expired",
        )

    user_repo = UserRepository()
    user = await user_repo.get(db, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    return user
