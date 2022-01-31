from typing import List

import loguru
from fastapi import APIRouter, HTTPException

from ..validation_models.movies import MovieOut, MovieIn, MovieUpdate
from ..models.movies import Movies
from ..core.db_manager import DBManager
from ..core.service import is_cast_present

movies = APIRouter()

db = DBManager()


@movies.post('/', response_model=MovieOut, status_code=201)
async def create_movie(payload: MovieIn):
    for cast_id in payload.casts_id:
        if not is_cast_present(cast_id):
            raise HTTPException(status_code=404, detail=f"Cast with given id:{cast_id} not found")

    movie_id = await db.fetch_one(Movies.__table__.insert().values(**payload.dict()))

    response = {
        'id': movie_id.id,
        **payload.dict()
    }

    return response


@movies.get('/', response_model=List[MovieOut])
async def get_movies():
    return await db.fetch_all(Movies.__table__.select())


@movies.get('/{movie_id}/', response_model=MovieOut)
async def get_movie(movie_id: int):
    movie = await db.fetch_one(Movies.__table__.select().where(Movies.id == movie_id))
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")
    return movie


@movies.put('/{movie_id}/', response_model=MovieOut)
async def update_movie(movie_id: int, payload: MovieUpdate):
    movie = await db.fetch_one(Movies.__table__.select().where(Movies.id == movie_id))
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")

    movie_in_db = MovieIn(**movie)
    update_data = payload.dict(exclude_unset=True)
    updated_movie = movie_in_db.copy(update=update_data)

    if 'casts_id' in update_data:
        for cast_id in payload.casts_id:
            if not is_cast_present(cast_id):
                raise HTTPException(status_code=404, detail=f"Cast with given id:{cast_id} not found")

    await db.execute(Movies.__table__.update().where(Movies.id == movie_id).values(**updated_movie.dict()))

    updated_movie = updated_movie.dict()
    updated_movie['id'] = movie_id
    return updated_movie


@movies.delete('/{movie_id}/', response_model=None)
async def delete_movie(movie_id: int):
    if await get_movie(movie_id):
        await db.execute(Movies.__table__.delete().where(Movies.id == movie_id))
