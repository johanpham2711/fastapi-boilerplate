import json
from typing import Any, Optional
import redis.asyncio as redis
from app.core.config import settings


class CacheService:
    def __init__(self):
        self._redis: Optional[redis.Redis] = None

    async def connect(self):
        if not self._redis:
            self._redis = await redis.from_url(
                f"redis://{settings.redis_host}:{settings.redis_port}",
                password=settings.redis_password if settings.redis_password else None,
                db=settings.redis_db,
                decode_responses=True,
            )

    async def disconnect(self):
        if self._redis:
            await self._redis.close()
            self._redis = None

    async def get(self, key: str) -> Optional[str]:
        await self.connect()
        return await self._redis.get(key)

    async def set(self, key: str, value: Any, ttl: Optional[int] = None):
        await self.connect()
        if isinstance(value, (dict, list)):
            value = json.dumps(value)
        
        if ttl:
            await self._redis.setex(key, ttl, value)
        else:
            await self._redis.set(key, value)

    async def delete(self, key: str):
        await self.connect()
        await self._redis.delete(key)

    async def exists(self, key: str) -> bool:
        await self.connect()
        return await self._redis.exists(key) > 0

    async def set_blacklist_token(self, token: str, ttl: int = 3600):
        await self.set(f"blacklist:{token}", "1", ttl)

    async def is_token_blacklisted(self, token: str) -> bool:
        return await self.exists(f"blacklist:{token}")


cache_service = CacheService()

