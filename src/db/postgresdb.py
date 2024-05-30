from typing import Optional

import asyncpg

from src.core.settings import psgr_settings

postgresdb: Optional[asyncpg.Connection] = None


async def get_postgres() -> asyncpg.Connection:
    return await asyncpg.connect(user=psgr_settings.user,
                                 host=psgr_settings.host,
                                 port=psgr_settings.port,
                                 password=psgr_settings.password,
                                 database=psgr_settings.database)








