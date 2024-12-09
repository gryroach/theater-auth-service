from sqlalchemy import Column, DateTime, ForeignKey, String
from sqlalchemy.sql import func
from werkzeug.security import check_password_hash, generate_password_hash

from db.db import Base


class User(Base):
    login = Column(String(255), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    first_name = Column(String(50))
    last_name = Column(String(50))
    created_at = Column(DateTime, default=func.now())

    def __init__(
        self, login: str, password: str, first_name: str, last_name: str
    ) -> None:
        self.login = login
        self.password = generate_password_hash(password)
        self.first_name = first_name
        self.last_name = last_name

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password, password)

    def __repr__(self) -> str:
        return f"<User {self.login}>"


class LoginHistory(Base):
    user_id = Column(String, ForeignKey("user.id"), nullable=False)
    ip_address = Column(String(50))
    user_agent = Column(String(255))
    login_time = Column(DateTime, default=func.now())
