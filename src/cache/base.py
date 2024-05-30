from abc import ABC, abstractmethod


class AsyncCache(ABC):
    @abstractmethod
    async def get_value(self, table: str):
        pass

    @abstractmethod
    async def set_value(self, *args, **kwargs):
        pass
