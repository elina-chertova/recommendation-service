from http import HTTPStatus

import aiohttp

from src.core.settings import AuthSettings

conf = AuthSettings()


async def get_user(request):
    async with aiohttp.ClientSession() as session:
        async with session.get(f"http://{conf.auth_service_host}:{conf.auth_service_port}/get_user_id",
                               headers=request.headers) as response:
            message = await response.json()
            user = message.get("user_id", None)
            code = response.status
            if code == HTTPStatus.FORBIDDEN:
                return message.get("description"), HTTPStatus.FORBIDDEN
            elif user:
                return user, HTTPStatus.OK
            elif code == HTTPStatus.UNAUTHORIZED or message.get("msg", None):
                return message.get("msg"), HTTPStatus.UNAUTHORIZED


