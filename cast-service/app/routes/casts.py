from typing import List

from fastapi import APIRouter, HTTPException
from sqlalchemy.engine import Row

from ..core.db_manager import DBManager
from ..validation_models.casts import CastOut, CastIn
from ..models.casts import Casts

casts = APIRouter()


db = DBManager()


@casts.get('/', response_model=List[CastOut])
async def get_casts():
    return await db.fetch_all(Casts.__table__.select())


@casts.post('/', response_model=CastOut, status_code=201)
async def create_cast(payload: CastIn):
    cast_id = await db.fetch_one(Casts.__table__.insert().values(**payload.dict()))

    response = {
        'id': cast_id.id,
        **payload.dict()
    }

    return response


@casts.get('/{cast_id}/', response_model=CastOut)
async def get_cast(cast_id: int):
    cast: Row = await db.fetch_one(Casts.__table__.select().where(Casts.id == cast_id))
    if not cast:
        raise HTTPException(status_code=404, detail="Cast not found")
    return cast


@casts.delete('/{cast_id}/')
async def get_cast(cast_id: int):
    if await get_cast(cast_id):
        await db.execute(Casts.__table__.delete().where(Casts.id == cast_id))
