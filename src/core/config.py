from logging import config as logging_config

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

from core.logger import LOGGING

logging_config.dictConfig(LOGGING)


class AppSettings(BaseSettings):
    project_name: str = Field(default="Movies auth API")

    # Настройки Postgres
    postgres_user: str = Field(default="postgres")
    postgres_password: str = Field(default="pass")
    postgres_host: str = Field(default="db")
    postgres_port: int = Field(default=5432)
    postgres_db: str = Field(default="movies_auth")
    echo_queries: bool = Field(default=False)

    # Настройки Redis
    redis_host: str = Field(default="redis")
    redis_port: int = Field(default=6379)

    # Настройки аутентификации
    ACCESS_TOKEN_EXPIRE_DAYS: int = Field(default=7)
    REFRESH_TOKEN_EXPIRE_DAYS: int = Field(default=30)
    secret_key: str = Field(default="your_secret_key")
    jwt_algorithm: str = Field(default="HS256")

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
    )

    @property
    def database_dsn(self) -> str:
        return (
            f"postgresql+asyncpg://{self.postgres_user}:"
            f"{self.postgres_password}@"
            f"{self.postgres_host}:"
            f"{self.postgres_port}/{self.postgres_db}"
        )


settings = AppSettings()
