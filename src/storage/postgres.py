
import asyncpg

from src.storage.base import AsyncStorage


class PostgreSQL(AsyncStorage):
    def __init__(self,
                 db: asyncpg.Connection):
        self.db = db

    async def insert(self,
                     query: str,
                     data: tuple):
        await self.db.execute(query, *data)

    async def get(self,
                  query: str):
        rows = await self.db.fetch(query)
        return rows


