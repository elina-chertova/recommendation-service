from typing import Optional

import aioredis
from aioredis import Redis

from src.core.settings import RedisSettings

redis_settings = RedisSettings()

redis: Optional[Redis] = None


async def get_redis() -> Redis:
    return await aioredis.from_url("redis://{0}:{1}".format(redis_settings.redis_host, redis_settings.redis_port))


