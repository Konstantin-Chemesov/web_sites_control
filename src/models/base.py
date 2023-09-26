from sqlalchemy.orm import declarative_base
from sqlalchemy import  Column, Integer, String, Time
from core import config
from sqlalchemy import create_engine
from sqlmodel import SQLModel, Field, TIME
import datetime
import time


Base = declarative_base()

class LinksBaseModel(SQLModel):
    link: str
    created_at: int


class Links(LinksBaseModel, table=True):
    id: int = Field(default=None, primary_key=True)


class SongCreate(LinksBaseModel):
    pass