from http import HTTPStatus

from fastapi import APIRouter, Depends

from src.core.messages import message
from src.core.settings import recs
from src.models.codes import Success
from src.models.cold_start import Genre, Movie
from src.services.cold_start import ColdStart, get_cold_start_service
from src.services.recommendations import Recommendation


router = APIRouter()


def get_recommend_service():
    return Recommendation()


@router.post('/select/movies',
             summary="Cold start",
             response_description="",
             description="Find preferable movies during cold start.")
async def select_movies_cs(genres: list[Genre],
                           cs: ColdStart = Depends(get_cold_start_service)) -> list[Movie]:

    movies = await cs.select_movies(genres=genres)
    return movies


@router.post('/find/recommend',
             summary="Cold start",
             response_description="",
             description="Create cold start recommendations.")
async def find_recommend_cs(movies: list[Movie],
                            user_id: str,
                            cs: ColdStart = Depends(get_cold_start_service),
                            rec: Recommendation = Depends(get_recommend_service)):
    movies_ = await cs.add_cs_movies(user_id=user_id, movies=movies)
    recommendations, valid_movie_ids = await cs.recommend(movies=movies_)

    await rec.add_rec_history(user_id=user_id, movies=recommendations, recommend_type=recs.cold_start)
    await rec.add_cache(rec_type=recs.cold_start, user_id=user_id, values=recommendations)

    return Success(message=message.rec_added, code=HTTPStatus.OK)
