from abc import ABC, abstractmethod
from typing import Any
from redis.asyncio import Redis

class CacheRepository(ABC):
    @abstractmethod
    async def get(self, key: str) -> Any:
        raise NotImplementedError

    @abstractmethod
    async def set(self, key: str, value: Any, expire: int | None = None) -> None:
        raise NotImplementedError


class RedisCacheRepository(CacheRepository):
    def __init__(self, redis: Redis):
        self.redis = redis

    async def get(self, key: str):
        return await self.redis.get(key)

    async def set(self, key: str, value: str, expire: int | None = None):
        await self.redis.set(key, value, ex=expire)