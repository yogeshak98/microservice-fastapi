from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Casts(Base):
    __tablename__ = 'casts'

    id = Column('id', Integer, primary_key=True)
    name = Column('name', String(50))
    nationality = Column('nationality', String(20))
