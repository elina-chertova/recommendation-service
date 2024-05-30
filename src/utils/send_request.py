import aiohttp


async def send_get_request(url: str,
                           headers=None,
                           params=None):
    if headers is None:
        headers = {}
    if params is None:
        params = {}
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers, params=params) as response:
            message = await response.json()
            code = response.status
            return message, code
