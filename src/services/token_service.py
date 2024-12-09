from fastapi import Depends
from redis.asyncio import Redis

from db.redis import get_redis
from repositories.cache import CacheRepository, RedisCacheRepository


class TokenService:
    def __init__(self, cache: CacheRepository):
        self.cache = cache

    async def set_session_version(self, user_id: str, version: int):
        key = f"session_version:{user_id}"
        await self.cache.set(key, version)

    async def get_session_version(self, user_id: str) -> int | None:
        key = f"session_version:{user_id}"
        return await self.cache.get(key)

    async def invalidate_session(self, user_id: str):
        key = f"session_version:{user_id}"
        await self.cache.delete(key)


async def get_token_service(redis: Redis = Depends(get_redis)) -> TokenService:
    cache = RedisCacheRepository(redis)
    return TokenService(cache=cache)
