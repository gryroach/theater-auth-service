from datetime import datetime, timedelta, timezone

import jwt

from core.config import settings


class JWTService:
    def __init__(self):
        with open(settings.private_key, "r") as private_key_file:
            self.private_key = private_key_file.read()
        with open(settings.public_key, "r") as public_key_file:
            self.public_key = public_key_file.read()
        self.algorithm = settings.jwt_algorithm
        self.access_token_expire = timedelta(
            days=settings.ACCESS_TOKEN_EXPIRE_DAYS
        )
        self.refresh_token_expire = timedelta(
            days=settings.REFRESH_TOKEN_EXPIRE_DAYS
        )

    def _create_token(self, payload: dict) -> str:
        """Создает JWT-токен с подписью приватным ключом (асимметричный)."""
        return jwt.encode(payload, self.private_key, algorithm=self.algorithm)

    def create_access_token(
            self, user_id: str, session_version: int, role: str
    ) -> str:
        now = datetime.now(timezone.utc)
        payload = {
            "user": user_id,
            "session_version": session_version,
            "iat": now,
            "exp": now + self.access_token_expire,
            "role": role,
            "type": "access",
        }
        return self._create_token(payload)

    def create_refresh_token(
            self, user_id: str, session_version: int, role: str
    ) -> str:
        now = datetime.now(timezone.utc)
        payload = {
            "user": user_id,
            "session_version": session_version,
            "iat": now,
            "exp": now + self.refresh_token_expire,
            "role": role,
            "type": "refresh",
        }
        return self._create_token(payload)

    def decode_token(self, token: str) -> dict:
        """
        Декодирует JWT-токен с использованием публичного ключа (асимметричный).
        """
        return jwt.decode(
            token, self.public_key, algorithms=[self.algorithm], verify=True
        )


def get_jwt_service() -> JWTService:
    """Создает экземпляр сервиса JWT."""
    return JWTService()
