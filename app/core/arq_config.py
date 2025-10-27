from arq import create_pool
from arq.connections import RedisSettings
from app.core.config import settings


redis_settings = RedisSettings(
    host=settings.redis_host,
    port=settings.redis_port,
    password=settings.redis_password if settings.redis_password else None,
    database=settings.redis_db,
)


async def get_redis_pool():
    return await create_pool(redis_settings)

