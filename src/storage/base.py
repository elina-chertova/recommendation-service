from abc import ABC, abstractmethod


class AsyncStorage(ABC):
    @abstractmethod
    async def get(self, table: str):
        pass

    @abstractmethod
    async def insert(self, *args, **kwargs):
        pass
