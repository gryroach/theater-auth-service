import asyncio
from functools import wraps

import typer

from db.db import Base, engine

app = typer.Typer()


def coro(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        return asyncio.run(f(*args, **kwargs))

    return wrapper


@app.command()
@coro
async def create_database() -> None:
    # Импортирование всех моделей
    import models  # noqa: F401

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


@app.command()
@coro
async def purge_database() -> None:
    # Импортирование всех моделей
    import models  # noqa: F401

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


if __name__ == "__main__":
    app()
