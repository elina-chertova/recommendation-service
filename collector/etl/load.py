import datetime

import asyncpg

from backoff.backoff import retry_on_error
from src.core.logger import logger
from src.core.messages import message
from src.core.settings import Endpoints, RecHistory, recs
from src.db.postgresdb import get_postgres
from src.rec_sys.content_based import ContentBased
from src.rec_sys.item_based import ItemBased
from src.services.helper import ContentHelper, ItemHelper
from src.services.recommendations import Recommendation
from src.storage.postgres import PostgreSQL


class Loader:
    def __init__(self):
        self.cb = ContentBased()
        self.ib = ItemBased()
        self.ih = ItemHelper()
        self.ch = ContentHelper()
        self.urls = Endpoints()
        self.recommend = Recommendation()
        self.rec_types = RecHistory()

    @staticmethod
    @retry_on_error()
    async def _add_rec_history(movies: list,
                               type_: str,
                               user_id: str) -> None:
        """
        Insert data into recommendation.history.
        :param movies:
        :param type_:
        :param user_id:
        :return:
        """
        db = await get_postgres()
        pg = PostgreSQL(db)

        query = """INSERT INTO recommendation.history (rec_type, date_recommend, user_id, movies, movie_ids)
                   VALUES ($1, $2, $3, $4, $5)"""
        date_recommend = datetime.date.today()
        try:
            await pg.insert(query, (type_, date_recommend, user_id, movies, []))
            logger.info(message.data_inserted.format("recommendation.history"))
        except asyncpg.exceptions.PostgresSyntaxError as e:
            logger.error(message.error_insert.format(e))

    async def _get_rec_item(self,
                            movies: list) -> list:
        """
        Get recommendations.
        :param movies:
        :return:
        """
        recs = self.ih.get_recommendation(titles=movies)
        return recs

    async def _get_rec_content(self,
                               movies: list) -> list:
        """
        Get recommendations.
        :param movies:
        :return:
        """
        recs = self.ch.get_recommendation(title=movies[0])
        return recs

    async def load_process(self,
                           user_movies: dict[str, list],
                           rec_type: str) -> None:
        """
        Load data into rec. history and cache.
        :param user_movies:
        :param rec_type:
        :return:
        """
        recs_ = []
        for user, movies in user_movies.items():
            if rec_type == recs.item_based:
                recs_ = await self._get_rec_item(movies=movies)
            elif rec_type == recs.have_already_watched_type:
                recs_ = await self._get_rec_content(movies=movies)
            else:
                logger.error(message.wrong_type.format(rec_type))

            if recs_:
                await self._add_rec_history(movies=recs_, type_=rec_type, user_id=user)
                await self.recommend.add_cache(rec_type=rec_type, user_id=user, values=recs_)
            else:
                logger.info(message.no_rec_user.format(user))






