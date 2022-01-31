import os

import sqlalchemy
from aiopg.sa import create_engine, Engine
from aiopg.sa.result import ResultProxy

uri = os.getenv('DATABASE_URI')
pool_size = int(os.getenv('POOL_SIZE', default=5))
engine = sqlalchemy.create_engine(uri, pool_size=1)


class Singleton(type):
    """
    Singleton metaclass implementation for python objects.
    This class will keep an _instance variable in **class** variable.
    This will make sure only one instance of object will be maintained.
    """

    def __init__(cls, *args, **kwargs):
        super().__init__(*args, **kwargs)
        cls._instance = None

    def __call__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__call__(*args, **kwargs)
        return cls._instance


class DBManager(metaclass=Singleton):
    def __init__(self):
        self.async_engine: Engine = None

    async def set_async_engine(self):
        self.async_engine: Engine = await create_engine(uri, minsize=pool_size)

    async def execute(self, query_statement, **kwargs):
        if self.async_engine is None:
            await self.set_async_engine()
        async with self.async_engine.acquire() as conn:
            await conn.execute(query=query_statement, **kwargs)

    async def fetch_all(self, query_statement, **kwargs):
        if self.async_engine is None:
            await self.set_async_engine()
        async with self.async_engine.acquire() as conn:
            results: ResultProxy = await conn.execute(query=query_statement, **kwargs)
            return await results.fetchall()

    async def fetch_one(self, query_statement, **kwargs):
        if self.async_engine is None:
            await self.set_async_engine()
        async with self.async_engine.acquire() as conn:
            results: ResultProxy = await conn.execute(query=query_statement, **kwargs)
            return await results.fetchone()


def create_table(base):
    base.__table__.create(engine)
