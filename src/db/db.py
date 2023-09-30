from sqlmodel import SQLModel
from core import config
import os

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from utils.logger import log

db_name = config.DB_NAME
is_testing = int(os.getenv('TEST', 0))
if is_testing:
    db_name = 'db_test'
engine = create_async_engine(
    f'''postgresql+asyncpg://{config.DB_USERNAME}:{config.DB_PASSWORD}@{config.PROJECT_HOST}:{config.DB_PORT}/{db_name}''',
        echo=True, query_cache_size=0,)

async def init_db():
    try:
        async with engine.begin() as conn:
            await conn.run_sync(SQLModel.metadata.create_all)
            log.info('Tables created')
    except ConnectionRefusedError as ex:
        log.warning(ex)


async def get_session() -> AsyncSession:
    try:
        async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
        async with async_session() as session:
            yield session
    except ConnectionRefusedError as ex:
        log.warning(ex)