import os

from dotenv import load_dotenv
from pydantic import BaseSettings, Field

load_dotenv()


class RecHistory:
    cold_start = "cold_start"
    have_already_watched_type = "content_based"
    item_based = "item_based"


class API:
    ugc_host = os.getenv("UGC_HOST", '127.0.0.1')
    ugc_port = os.getenv("UGC_PORT", '8003')
    async_host = os.getenv("ASYNC_HOST", '127.0.0.1')
    async_port = os.getenv("ASYNC_PORT", '8005')


api_ = API()


class Endpoints:
    ugc_views = f"http://{api_.ugc_host}:{api_.ugc_port}/api/v1/views/protected/history/views/watched"
    api_key = os.getenv("API_KEY")
    DROPBOX_ACCESS_TOKEN = os.getenv("DROPBOX_ACCESS_TOKEN")
    async_service = f"http://{api_.async_host}:{api_.async_port}/api/v1"
    genres = f"{async_service}/genres"
    movie_genre = f"{async_service}/films/"


class PostgresSettings(BaseSettings):
    user = Field('user', env='PSG_USER')
    password = Field('password', env='PSG_PWD')
    database = Field('database', env='PSG_DB')
    host = Field('127.0.0.1', env='PSG_HOST')
    port = Field('5432', env='PSG_PORT')


class RedisSettings(BaseSettings):
    redis_host = Field('127.0.0.1', env='REDIS_HOST')
    redis_port = Field('6379', env='REDIS_PORT')


class AuthSettings(BaseSettings):
    auth_service_host = Field('127.0.0.1', env='AUTH_SERVICE_HOST')
    auth_service_port = Field('5000', env="AUTH_SERVICE_PORT")


psgr_settings = PostgresSettings()
recs = RecHistory()
