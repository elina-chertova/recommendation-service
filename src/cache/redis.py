from typing import Optional

import aioredis

from src.cache.base import AsyncCache


class RedisClient(AsyncCache):
    def __init__(self,
                 redis: aioredis.Redis):
        self.redis = redis

    async def get_value(self,
                        key: str) -> str | None:
        value = await self.redis.get(key)
        decoded_output = value.decode() if value else None
        result = decoded_output.split(";;")
        return result

    async def set_value(self,
                        key: str,
                        value: str,
                        expiration: int) -> None:
        await self.redis.set(key, value, ex=86400)

