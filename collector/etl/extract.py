from collector.utils.helper import HelperExtractor
from src.core.settings import Endpoints
from src.utils.send_request import send_get_request


class Extractor(HelperExtractor):
    def __init__(self):
        self.urls = Endpoints()

    async def _get_views(self) -> tuple:
        """
        Get viewed movies for users.
        :return:
        """
        users, status_code = await send_get_request(
            url=self.urls.ugc_views,
            headers={"X-API-Key": self.urls.api_key}
        )
        return users, status_code

    async def item_based(self) -> dict[str, list[str]]:
        """
        Most viewed movies for each user.
        :return:
        """
        users, status_code = await self._get_views()
        user_movie, user_movie_count = self.count_duplicate_entries(users)
        sorted_user_movie_count = dict(sorted(user_movie_count.items()))
        users_movie = self.choose_users(user_movie=sorted_user_movie_count)
        return users_movie

    async def content_based(self) -> dict[str, list[str]]:
        """
        Data for 'have already watched' type.
        :return:
        """
        users_movies, status_code = await self._get_views()
        watched_movie = self.find_last_watched(users_movies=users_movies)
        return watched_movie
