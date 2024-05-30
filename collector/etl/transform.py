import uuid

import asyncpg

from backoff.backoff import retry_on_error
from src.core.logger import logger
from src.core.messages import message
from src.core.settings import Endpoints, RecHistory
from src.db.postgresdb import get_postgres
from src.storage.postgres import PostgreSQL
from src.utils.send_request import send_get_request


class Transformer:
    def __init__(self):
        self.urls = Endpoints()
        self.rec_types = RecHistory()

    @staticmethod
    async def _connection() -> PostgreSQL:
        db = await get_postgres()
        conn = PostgreSQL(db)
        return conn

    async def _get_title(self,
                         movie_id: str) -> str:
        """
        Movie ID to title.
        :param movie_id:
        :return:
        """
        movie, status_code = await send_get_request(url=self.urls.movie_genre + movie_id)
        title = movie["title"]
        return title

    async def get_user_title_movie(self,
                                   data: dict[str, list[str]]) -> dict[str, list[str]]:
        """
        Find movies' titles.
        :param data:
        :return:
        """
        user_movie = {}
        for user, movie in data.items():
            titles = []
            for m in movie:
                title = await self._get_title(m)
                titles.append(title)
            user_movie[user] = titles
        return user_movie

    @retry_on_error()
    async def find_cold_start_users(self,
                                    user_ids_exist: list[str]) -> dict[str, list[str]]:
        """
        Find users from cold start that not in ugc service.
        :param user_ids_exist:
        :return:
        """
        try:
            pg = await self._connection()
            user_ids_uuid = [uuid.UUID(id) for id in user_ids_exist]
            user_ids_str = ', '.join(f"'{id}'" for id in user_ids_uuid)

            query = f"SELECT user_id, movie_id, title FROM recommendation.cold_start " \
                    f"WHERE user_id NOT IN ({user_ids_str}) GROUP BY user_id, movie_id, title;"

            users_records = await pg.get(query)
            result = {}
            for record in users_records:
                if str(record['user_id']) in user_ids_exist:
                    continue
                user_id = str(record['user_id'])
                movie_titles = record['title']
                result[user_id] = movie_titles
            return result
        except asyncpg.exceptions.DataError as e:
            logger.error(message.error_find_user.format(e))
            return {}
