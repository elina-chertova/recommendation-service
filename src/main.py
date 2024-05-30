import logging

import uvicorn
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from contextlib import asynccontextmanager

from src.api.v1 import cold_start, recommend
from src.core.logger import LOGGING
from src.db import postgresdb, redis


@asynccontextmanager
async def lifespan(app: FastAPI):
    postgresdb.postgresdb = await postgresdb.get_postgres()
    redis.redis = await redis.get_redis()
    yield
    await postgresdb.postgresdb.close()


app = FastAPI(
    lifespan=lifespan,
    title='Recommendation service',
    docs_url='/api/openapi',
    openapi_url='/api/openapi.json',
    default_response_class=ORJSONResponse,
    description="Service to get users recommendations.",
    version="1.0.0"
)

app.include_router(recommend.router, prefix='/api/v1/recommend', tags=['recommendations'])
app.include_router(cold_start.router, prefix='/api/v1/coldstart', tags=['cold_start'])

if __name__ == '__main__':
    uvicorn.run(
        'main:app',
        host='0.0.0.0',
        port=8015,
        log_config=LOGGING,
        log_level=logging.DEBUG,
    )

