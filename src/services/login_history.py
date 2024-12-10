from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from repositories.login_history import LoginHistoryRepository
from schemas.entity import LoginHistoryCreate


class LoginHistoryService:
    def __init__(self, repo: LoginHistoryRepository):
        self.repo = repo

    async def log_login(self, db: AsyncSession, data: LoginHistoryCreate):
        """Записать вход в историю."""
        return await self.repo.create(db, obj_in=data)

    async def get_user_history(self, db: AsyncSession, user_id: str):
        """Получить историю входов для конкретного пользователя."""
        return await self.repo.get_by_field_multi(
            db, field="user_id", value=user_id, skip=0, limit=100
        )


async def get_login_history_service(
    repo: LoginHistoryRepository = Depends(),
) -> LoginHistoryService:
    return LoginHistoryService(repo=repo)
