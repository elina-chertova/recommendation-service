from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException, Query, Request

from src.services.recommendations import Recommendation
from src.utils.check_data.check_auth import get_user

router = APIRouter()


def get_recommend():
    return Recommendation()


@router.get('/item-based',
            summary="Item-based recommendations.",
            response_description="User's recommendations.")
async def user_item_based(request: Request, rec_type: str = Query("item_based", description="Recommendation type"),
                          rec_sys: Recommendation = Depends(get_recommend)):
    user, user_code = await get_user(request)
    if user_code == HTTPStatus.OK:
        result = await rec_sys.get_cache(user_id=user, rec_type=rec_type)
        return result
    raise HTTPException(status_code=user_code, detail=user)


@router.get('/content-based',
            summary="Content-based recommendations.",
            response_description="User's recommendations.")
async def user_content_based(request: Request,
                             rec_type: str = Query("content_based", description="Recommendation type"),
                             rec_sys: Recommendation = Depends(get_recommend)):
    user, user_code = await get_user(request)
    if user_code == HTTPStatus.OK:
        result = await rec_sys.get_cache(user_id=user, rec_type=rec_type)
        return result
    raise HTTPException(status_code=user_code, detail=user)
