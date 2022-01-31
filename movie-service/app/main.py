import os

from fastapi import FastAPI
from loguru import logger
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.ext.automap import automap_base

from .core.db_manager import DBManager
from .routes.movies import movies

app = FastAPI(openapi_url="/api/v1/movies/openapi.json", docs_url="/api/v1/movies/docs")


@app.on_event("startup")
async def startup():
    logger.info('Starting movies-service microservice!!!')
    engine: Engine = create_engine(os.getenv("DATABASE_URI"), pool_size=1)
    automap_base().prepare(engine, reflect=True)
    engine.dispose()
    DBManager()



@app.on_event("shutdown")
async def shutdown():
    logger.info("Shutting movies-service microservice!!!")
    DBManager().async_engine.close()


app.include_router(movies, prefix='/api/v1/movies', tags=['movies'])
