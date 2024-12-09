from db.redis import get_redis
from repositories.cache import CacheRepository, RedisCacheRepository


class TokenService:
    default_cache: CacheRepository

    def __init__(self, cache: CacheRepository = None):
        if cache is None:
            if not hasattr(TokenService, "default_cache"):
                raise ValueError("Cache repository is not initialized.")
            self.cache = TokenService.default_cache
        else:
            self.cache = cache

    @classmethod
    async def initialize_default_cache(cls):
        """Инициализация Redis по умолчанию для использования в TokenService"""
        redis = await get_redis()
        cls.default_cache = RedisCacheRepository(redis)

    async def set_session_version(self, user_id: str, version: int):
        key = f"session_version:{user_id}"
        await self.cache.set(key, version)

    async def get_session_version(self, user_id: str) -> int | None:
        key = f"session_version:{user_id}"
        return await self.cache.get(key)

    async def invalidate_session(self, user_id: str):
        key = f"session_version:{user_id}"
        await self.cache.delete(key)
