from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class UserCreate(BaseModel):
    login: str
    password: str
    first_name: str
    last_name: str


class UserInDB(BaseModel):
    id: UUID
    first_name: str
    last_name: str

    class Config:
        from_attributes = True


class LoginHistoryCreate(BaseModel):
    user_id: UUID
    ip_address: str | None
    user_agent: str | None


class LoginHistoryInDB(LoginHistoryCreate):
    login_time: datetime

    class Config:
        from_attributes = True


class LoginRequest(BaseModel):
    login: str
    password: str


class LoginResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"

    class Config:
        from_attributes = True
