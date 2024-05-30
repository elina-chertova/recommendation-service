import asyncio

from apscheduler.schedulers.asyncio import AsyncIOScheduler

from collector.etl.extract import Extractor
from collector.etl.load import Loader
from collector.etl.transform import Transformer
from collector.utils.triggers import tasks_trigger
from src.core.logger import logger
from src.core.settings import recs


class ETL:
    def __init__(self, trigger: dict):
        self.extract = Extractor()
        self.transform = Transformer()
        self.load = Loader()
        self.trigger = trigger

    async def run_item_based(self) -> None:
        user_movies = await self.extract.item_based()
        user_movie_fpart = await self.transform.get_user_title_movie(user_movies)
        user_movie_spart = await self.transform.find_cold_start_users(user_ids_exist=list(user_movie_fpart.keys()))
        try:
            user_movie_fpart.update(user_movie_spart)
            await self.load.load_process(user_movies=user_movie_fpart, rec_type=recs.item_based)
        except TypeError as e:
            logger.info("Can't update dict: {0}".format(e))

    async def run_content_based(self):
        user_movies = await self.extract.content_based()
        user_movie_fpart = await self.transform.get_user_title_movie(user_movies)
        await self.load.load_process(user_movies=user_movie_fpart, rec_type=recs.have_already_watched_type)

    async def __call__(self):
        scheduler = AsyncIOScheduler()
        scheduler.start()

        scheduler.add_job(
            self.run_item_based,
            trigger=self.trigger["item.based"],
            name=recs.item_based,
        )
        scheduler.add_job(
            self.run_content_based,
            trigger=self.trigger["content.based"],
            name=recs.have_already_watched_type,
        )
        try:
            while True:
                await asyncio.sleep(1)
        except (KeyboardInterrupt, SystemExit):
            scheduler.shutdown()


if __name__ == "__main__":
    etl = ETL(trigger=tasks_trigger)
    asyncio.run(etl())

