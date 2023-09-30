import os
import pytest
from httpx import AsyncClient
import asyncio
import time
from sqlalchemy import inspect

os.environ['TEST'] = '1'
from main import app
from db.db import init_db

from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database
from core import config

engine = create_engine(
    f'''postgresql://{config.DB_USERNAME}:{config.DB_PASSWORD}@{config.PROJECT_HOST}:{config.DB_PORT}/db_test''')
if not database_exists(engine.url):
    create_database(engine.url)

test_domain_name = 'test_domain_main_main.ru'


@pytest.fixture(scope="module")
async def test_app():
    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client

@pytest.mark.anyio
async def test_first_page_get_positive(test_app: AsyncClient):
    """ Тестирование работоспособности сервера """
    response = await test_app.get("/")
    assert response.status_code == 200

@pytest.mark.anyio
async def test_tables_creation():
    """ Тестирование создания таблиц в БД """
    await init_db()
    inspector = inspect(engine)
    tables = inspector.get_table_names()
    assert 'links' in tables

@pytest.mark.anyio
async def test_linksroute_post_positive(test_app: AsyncClient):
    """ Тестирование ендпоинта для записи новых веб-адресов в базу """
    response = await test_app.post("/visited_links", json={"links": [f"https://{test_domain_name}/"]})
    assert response.status_code == 200
    assert response.json() == {'status': 'ok'}

@pytest.mark.anyio
async def test_linksroute_get_positive(test_app: AsyncClient):
    """ Тестирование работоспособности сервера """
    response = await test_app.get(f"/visited_links?time_from={time.time()-10}&time_to={time.time()}")
    assert response.status_code == 200 
    assert test_domain_name in response.json()['domains']

os.environ['TEST'] = '0'
