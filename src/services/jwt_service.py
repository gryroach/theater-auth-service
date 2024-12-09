from datetime import datetime, timedelta, timezone

import jwt

from core.config import settings


class JWTService:
    def __init__(self, secret: str, algorithm: str):
        self.secret = secret
        self.algorithm = algorithm

    def create_access_token(
        self, user_id: str, session_version: int, expires_delta: timedelta
    ):
        now = datetime.now(timezone.utc)
        payload = {
            "user": user_id,
            "session_version": session_version,
            "iat": now,
            "exp": now + expires_delta,
        }
        return jwt.encode(payload, self.secret, algorithm=self.algorithm)

    def create_refresh_token(
        self, user_id: str, session_version: int, expires_delta: timedelta
    ):
        now = datetime.now(timezone.utc)
        payload = {
            "user": user_id,
            "session_version": session_version,
            "iat": now,
            "exp": now + expires_delta,
        }
        return jwt.encode(payload, self.secret, algorithm=self.algorithm)

    def decode_token(self, token: str):
        return jwt.decode(token, self.secret, algorithms=[self.algorithm])


def get_jwt_service() -> JWTService:
    return JWTService(
        secret=settings.secret_key,
        algorithm=settings.jwt_algorithm,
    )
