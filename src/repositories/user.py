from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models import User
from repositories.base import RepositoryDB
from schemas.entity import UserCreate, UserInDB


class UserRepository(RepositoryDB[User, UserCreate, UserInDB]):
    def __init__(self):
        super().__init__(User)

    async def get_by_field(self, db: AsyncSession, field: str, value: str):
        statement = select(self._model).where(getattr(self._model, field) == value)
        result = await db.execute(statement)
        return result.scalar_one_or_none()
