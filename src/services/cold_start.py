import random
import uuid
from functools import lru_cache

import asyncpg
from fastapi import Depends

from src.core.logger import logger
from src.core.messages import message
from src.core.settings import Endpoints
from src.db.postgresdb import get_postgres
from src.models.cold_start import Genre, Movie
from src.services.helper import ItemHelper
from src.storage.base import AsyncStorage
from src.storage.postgres import PostgreSQL


class ColdStart(ItemHelper):
    def __init__(self, storage: AsyncStorage):
        super().__init__()
        self.storage = storage
        self.urls = Endpoints()
        self.rec_number = 10
        self.rec_movies = 40
        self.genre_page_size = 50

    async def select_movies(self,
                            genres: list[Genre]) -> list[Movie]:
        """
        Selects a list of movies from the specified genres.
        :param genres:
        :return:
        """
        all_movies = []

        for genre in genres:
            try:
                movies = await self.simplified_algo(genre=genre.name, page_size=self.genre_page_size)
                result_movies = [Movie(id=movie['id'], title=movie['title']) for movie in movies]
                all_movies.append(result_movies)
            except Exception as e:
                logger.error(message.error_select_movie.format(e))

        flattened_all_movies = [item for sublist in all_movies for item in sublist]
        result_movies = random.sample(flattened_all_movies, self.rec_movies)
        return result_movies

    async def add_cs_movies(self,
                            user_id: str,
                            movies: list[Movie]) -> list:
        """
        Adds cold start movies for a user.
        :param user_id:
        :param movies:
        :return:
        """
        query = """
                INSERT INTO recommendation.cold_start (id, user_id, movie_id, title)
                VALUES ($1, $2, $3, $4)
            """
        movies_list, movie_ids = [], []
        for item in movies:
            movie_ids.append(item.id)
            movies_list.append(item.title)
        try:
            await self.storage.insert(query, (uuid.uuid4(), user_id, movie_ids, movies_list))
            logger.info(message.data_inserted.format("recommendation.cold_start"))
        except asyncpg.exceptions.DataError as e:
            logger.error(message.wrong_user_id.format(e))
        except Exception as e:
            logger.error(message.error_add_movie.format(str(e)))
        return movies_list

    async def recommend(self,
                        movies: list[str],
                        valid_movie_ids=None) -> tuple:
        """
        Generates recommendations based on the specified movies.
        :param movies:
        :param valid_movie_ids:
        :return:
        """
        if valid_movie_ids is None:
            valid_movie_ids = []
        recommend, valid_movie_ids = self.get_recommendation(movies), valid_movie_ids
        return recommend, valid_movie_ids


@lru_cache()
def get_cold_start_service(
    db: asyncpg.Connection = Depends(get_postgres),
) -> ColdStart:
    storage = PostgreSQL(db)
    return ColdStart(storage)
