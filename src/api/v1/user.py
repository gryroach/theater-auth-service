from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from db.db import get_session
from db.redis import get_redis
from repositories.user import UserRepository
from schemas.entity import UserCreate, UserInDB
from services.token_service import TokenService
from repositories.cache import RedisCache

router = APIRouter()

@router.post(
    "/signup",
    response_model=UserInDB,
    status_code=status.HTTP_201_CREATED,
)
async def create_user(
    user_create: UserCreate, 
    db: AsyncSession = Depends(get_session),
    redis = Depends(get_redis)
) -> UserInDB:
    user_repo = UserRepository()
    token_service = TokenService(RedisCache(redis))
    
    existing_user = await user_repo.get_by_field(db, "login", user_create.login)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Login already exists"
        )

    user = await user_repo.create(db, obj_in=user_create)

    await token_service.set_session_version(str(user.id), 1)
    
    return user