import typer
from redis.asyncio import Redis
from typing_extensions import Annotated

from core.config import settings
from db.db import async_session
from exceptions import UserAlreadyExistsError
from repositories.cache import RedisCacheRepository
from repositories.user import UserRepository
from schemas.user import UserCreate
from services.session_service import SessionService
from services.user import UserService
from utils import coro

app = typer.Typer()


@app.command()
@coro
async def create_admin(
    login: Annotated[str, typer.Argument(help="Логин")],
    password: Annotated[str, typer.Argument(help="Пароль")],
    first_name: Annotated[str, typer.Argument(help="Имя")] = "",
    last_name: Annotated[str, typer.Argument(help="Фамилия")] = "",
) -> None:
    user_data = UserCreate(
        login=login,
        password=password,
        first_name=first_name,
        last_name=last_name,
    )
    user_repo = UserRepository()
    redis = Redis.from_url(settings.redis_url)
    try:
        token_service = SessionService(RedisCacheRepository(redis))
        user_service = UserService(
            user_repo=user_repo, session_service=token_service
        )
        async with async_session() as session:
            await user_service.register_user(db=session, user_data=user_data)
        print(f"Пользователь с логином {login} создан.")
    except UserAlreadyExistsError:
        print("Ошибка! Пользователь с таким логином уже существует.")
    finally:
        await redis.aclose()


if __name__ == "__main__":
    app()