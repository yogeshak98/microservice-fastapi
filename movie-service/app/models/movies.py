from sqlalchemy import (Column, Integer, String, ARRAY)
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Movies(Base):
    __tablename__ = "movies"

    id = Column('id', Integer, primary_key=True)
    name = Column('name', String(50))
    plot = Column('plot', String(250))
    genres = Column('genres', ARRAY(String))
    casts_id = Column('casts_id', ARRAY(Integer))
