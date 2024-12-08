from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.ext.declarative import as_declarative, declared_attr

from core.config import settings

@as_declarative()
class Base:
    """
    Базовый класс для всех ORM-моделей.
    """
    id: str
    __name__: str

    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__.lower()

engine = create_async_engine(
    settings.database_dsn, echo=settings.echo_queries, future=True
)
async_session = async_sessionmaker(engine, expire_on_commit=False)


async def get_session() -> AsyncSession:
    async with async_session() as session:
        yield session
