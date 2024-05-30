import datetime

import asyncpg

from src.cache.redis import RedisClient
from src.core.logger import logger
from src.core.messages import message
from src.core.settings import Endpoints
from src.db.postgresdb import get_postgres
from src.db.redis import get_redis
from src.services.helper import ItemHelper
from src.storage.postgres import PostgreSQL


class Recommendation(ItemHelper):
    def __init__(self):
        super().__init__()
        self.urls = Endpoints()
        self.item_helper = ItemHelper()

    @staticmethod
    async def _storage():
        db = await get_postgres()
        conn = PostgreSQL(db)
        return conn

    @staticmethod
    async def _cache():
        cache = await get_redis()
        conn = RedisClient(cache)
        return conn

    async def add_rec_history(self,
                              user_id: str,
                              movies: list,
                              recommend_type: str,
                              valid_movie_ids=None) -> None:
        """
        Adds a user's recommendation history to the storage.
        :param user_id:
        :param movies:
        :param recommend_type:
        :param valid_movie_ids:
        :return:
        """
        if valid_movie_ids is None:
            valid_movie_ids = []
        if not movies:
            logger.info(message.no_movie_to_rec)
            return
        storage = await self._storage()
        query = """
            INSERT INTO recommendation.history (rec_type, date_recommend, user_id, movies, movie_ids)
            VALUES ($1, $2, $3, $4, $5)
            """
        date_recommend = datetime.date.today()
        try:
            await storage.insert(query, (recommend_type, date_recommend, user_id, movies, valid_movie_ids))
            logger.info(message.data_inserted.format("recommendation.history"))
        except asyncpg.exceptions.DataError as e:
            logger.error(message.error_insert.format(e))

    async def add_cache(self,
                        rec_type: str,
                        user_id: str,
                        values: list,
                        rec_item: str = "movie") -> None:
        """
        Adds recommendations to the cache (Redis).
        :param rec_type:
        :param user_id:
        :param values:
        :param rec_item:
        :return:
        """
        value = ';;'.join(values)
        async with self._cache() as cache:
            key = "{0}::{1}::{2}".format(user_id, rec_item, rec_type)
            await cache.set_value(key=key, value=value, expiration=86400)
            logger.info(message.cache_inserted.format(key, value))

    async def get_cache(self,
                        rec_type: str,
                        user_id: str,
                        rec_item: str = "movie") -> list:
        """
        Retrieves recommendations from the cache (Redis).
        :param rec_type:
        :param user_id:
        :param rec_item:
        :return:
        """
        async with self._cache() as cache:
            key = "{0}::{1}::{2}".format(user_id, rec_item, rec_type)
            recommends = await cache.get_value(key=key)
            return recommends
