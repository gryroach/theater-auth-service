from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from repositories.user import UserRepository
from schemas.entity import UserCreate, UserInDB
from services.token_service import TokenService


class UserService:
    def __init__(
        self,
        user_repo: UserRepository,
        token_service: TokenService,
    ):
        self.user_repo = user_repo
        self.token_service = token_service

    async def register_user(
        self, db: AsyncSession, user_data: UserCreate
    ) -> UserInDB:
        existing_user = await self.user_repo.get_by_field(
            db, "login", user_data.login
        )
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Login already exists",
            )
        user = await self.user_repo.create(db, obj_in=user_data)
        await self.token_service.set_session_version(str(user.id), 1)
        return user
