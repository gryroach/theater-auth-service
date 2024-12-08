from sqlalchemy.ext.asyncio import AsyncSession
from repositories.user import UserRepository
from services.token_service import TokenService
from schemas.entity import UserCreate, UserInDB


class UserService:
    def __init__(self, user_repo: UserRepository, token_service: TokenService):
        self.user_repo = user_repo
        self.token_service = token_service

    async def register_user(self, db: AsyncSession, user_data: UserCreate) -> UserInDB:
        user = await self.user_repo.create(db, obj_in=user_data)
        await self.token_service.set_session_version(str(user.id), 1)
        return user