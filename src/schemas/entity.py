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
        orm_mode = True


class LoginHistoryCreate(BaseModel):
    user_id: str
    ip_address: str | None
    user_agent: str | None


class LoginHistoryInDB(LoginHistoryCreate):
    login_time: str


class LoginRequest(BaseModel):
    login: str
    password: str
    access_exp: int | None = None
    refresh_exp: int | None = None


class LoginResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"

    class Config:
        orm_mode = True
