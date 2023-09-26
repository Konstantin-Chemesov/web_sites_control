import os

from sqlmodel import SQLModel
from core import config

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL = os.environ.get("DATABASE_URL")

engine = create_async_engine(
    f"postgresql+asyncpg://postgres:postgres@0.0.0.0:5434/server_dbase", echo=True, future=True)

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)


async def get_session() -> AsyncSession:
    async_session = sessionmaker(
        engine, class_=AsyncSession, expire_on_commit=True
    )
    async with async_session() as session:
        yield session