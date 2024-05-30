import asyncio
from functools import wraps

import aioredis

from src.core.logger import logger


def retry_on_error(logger=logger, start_sleep_time=0.5, factor=2, border_sleep_time=10):
    """
    Function decorator for retrying a function after a certain delay if an error occurs.
    Uses a naive exponential backoff time (factor) up to the border sleep time (border_sleep_time).
    Formula:
        t = start_sleep_time * 2^(n) if t < border_sleep_time
        t = border_sleep_time if t >= border_sleep_time
    :param logger: logger
    :param start_sleep_time: initial sleep time
    :param factor: factor by which to increase the sleep time
    :param border_sleep_time: border sleep time
    :return: result of the function
    """
    def func_wrapper(func):
        @wraps(func)
        async def inner(*args, **kwargs):
            sleep_time = start_sleep_time
            cnt = 0
            max_tries = 5
            while True:
                try:
                    return await func(*args, **kwargs)
                except ConnectionRefusedError as e:
                    logger.error('Connection refused error. Error: {0}'.format(e))
                except aioredis.RedisError as e:
                    logger.error('Redis error: {0}.'.format(e))
                except Exception as e:
                    logger.error('Connection error: {}'.format(func.__name__), e)

                sleep_time = sleep_time * factor if sleep_time < border_sleep_time else border_sleep_time
                cnt += 1
                await asyncio.sleep(sleep_time)

                if cnt > max_tries:
                    logger.error(f"Tries were finished {func.__name__}")
                    break

        return inner

    return func_wrapper
