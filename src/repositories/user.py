from models import User
from repositories.base import RepositoryDB
from schemas.entity import UserCreate, UserInDB


class UserRepository(RepositoryDB[User, UserCreate, UserInDB]):
    def __init__(self):
        super().__init__(User)
