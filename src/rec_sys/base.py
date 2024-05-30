from abc import abstractmethod
from http import HTTPStatus

from src.core.logger import logger
from src.core.messages import message
from src.core.settings import Endpoints
from src.utils.send_request import send_get_request


class RecSystem:
    @abstractmethod
    def _load_model(self):
        pass

    @abstractmethod
    def recommendation(self, *args, **kwargs):
        pass

    @staticmethod
    async def simplified_algo(genre: str,
                              page_size: int = 10):
        """
        Get movies on genre.
        :param genre:
        :param page_size:
        :return:
        """
        urls = Endpoints()
        params = {
            "sort": "imdb_rating:desc",
            "genre": genre,
            "page[size]": page_size,
            "page[number]": 1
        }
        movies, status_code = await send_get_request(url=urls.movie_genre, params=params)
        if status_code == HTTPStatus.OK:
            return movies
        logger.info(message.error_request.format(urls.movie_genre))
        return None

