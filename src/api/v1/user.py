from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from db.db import get_session
from repositories.user import UserRepository
from schemas.entity import UserCreate, UserInDB
from services.token_service import TokenService
from services.user import UserService

router = APIRouter()


async def get_user_service() -> UserService:
    await TokenService.initialize_default_cache()
    token_service = TokenService()
    user_repo = UserRepository()
    return UserService(user_repo=user_repo, token_service=token_service)


@router.post(
    "/signup",
    response_model=UserInDB,
    status_code=status.HTTP_201_CREATED,
)
async def create_user(
    user_create: UserCreate,
    user_service: UserService = Depends(get_user_service),
    db: AsyncSession = Depends(get_session),
) -> UserInDB:
    user = await user_service.register_user(db, user_create)
    return user
