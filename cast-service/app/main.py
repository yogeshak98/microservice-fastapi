import os

from fastapi import FastAPI
from loguru import logger
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.ext.automap import automap_base

from .core.db_manager import DBManager
from .routes.casts import casts

app = FastAPI(openapi_url="/api/v1/casts/openapi.json", docs_url="/api/v1/casts/docs")


@app.on_event("startup")
async def startup():
    logger.info('Starting cast-service microservice!!!')
    engine: Engine = create_engine(os.getenv("DATABASE_URI"), pool_size=1)
    automap_base().prepare(engine, reflect=True)
    engine.dispose()
    DBManager()


@app.on_event("shutdown")
async def shutdown():
    logger.info("Shutting cast-service microservice!!!")
    DBManager().async_engine.close()


app.include_router(casts, prefix='/api/v1/casts', tags=['casts'])
