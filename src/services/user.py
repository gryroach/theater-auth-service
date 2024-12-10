from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from exceptions.user_exceptions import UserAlreadyExistsError
from repositories.user import UserRepository
from schemas.user import UserCreate, UserInDB
from services.token_service import TokenService, get_token_service


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
            raise UserAlreadyExistsError("Login already exists")
        user = await self.user_repo.create(db, obj_in=user_data)
        await self.token_service.set_session_version(str(user.id), 1)
        return user


async def get_user_service(
    user_repo: UserRepository = Depends(),
    token_service: TokenService = Depends(get_token_service),
) -> UserService:
    return UserService(user_repo=user_repo, token_service=token_service)
