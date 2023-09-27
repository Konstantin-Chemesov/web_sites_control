import os

from sqlmodel import SQLModel
from core import config

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from utils.logger import log

DATABASE_URL = os.environ.get("DATABASE_URL")

engine = create_async_engine(
    f"postgresql+asyncpg://postgres:postgres@0.0.0.0:5434/postgres", echo=True,
    query_cache_size=0,)

async def init_db():
    try:
        async with engine.begin() as conn:
            await conn.run_sync(SQLModel.metadata.create_all)
    except ConnectionRefusedError as ex:
        log.warning(ex)


async def get_session() -> AsyncSession:
    try:
        async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
        async with async_session() as session:
            yield session
    except ConnectionRefusedError as ex:
        log.warning(ex)