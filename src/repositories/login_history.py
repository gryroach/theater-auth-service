from models import LoginHistory
from repositories.base import RepositoryDB
from schemas.entity import LoginHistoryCreate, LoginHistoryInDB


class LoginHistoryRepository(
    RepositoryDB[LoginHistory, LoginHistoryCreate, LoginHistoryInDB]
):
    def __init__(self):
        super().__init__(LoginHistory)
