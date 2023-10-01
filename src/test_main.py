import os
import pytest
import time
from fastapi.testclient import TestClient

os.environ['TEST'] = '1'
from main import app

from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database, drop_database
from core import config

engine = create_engine(
    f'''postgresql://{config.DB_USERNAME}:{config.DB_PASSWORD}@{config.PROJECT_HOST}:{config.DB_PORT}/{config.DB_TEST_NAME}''')
if not database_exists(engine.url):
    create_database(engine.url)

test_domain_name = 'test_domain_main_main.ru'
test_domain_name_negative_test = 'test_domain_???main_main.ru'


@pytest.fixture(scope="module")
def test_app():
    with TestClient(app) as client:
        yield client
    if database_exists(engine.url):
        drop_database(engine.url)
    os.environ['TEST'] = '0'
    

def test_first_page_get_positive():
    """ Тестирование работоспособности сервера (контекстный менеджер для активации startup евента FastApi) """
    with TestClient(app) as client:
        response = client.get("/")
        assert response.status_code == 200


def test_linksroute_post_positive(test_app):
    """ Тестирование ендпоинта для записи новых веб-адресов в базу """
    response = test_app.post("/visited_links", json={"links": [f"https://{test_domain_name}/"]})
    assert response.status_code == 200
    assert response.json() == {'status': 'ok'}


def test_linksroute_post_negative(test_app):
    """ Тестирование ендпоинта для записи новых веб-адресов в базу """
    response = test_app.post("/visited_links", json={"links": [f"https://{test_domain_name_negative_test}/"]})
    assert response.status_code == 200
    assert 'неверный формат ссылки' in response.json()['status']


def test_linksroute_get_with_params_positive(test_app):
    """ Тестирование получения данных из базы с параметрами """
    response = test_app.get(f"/visited_links?time_from={time.time()-10000}&time_to={time.time()}")
    assert response.status_code == 200 
    assert test_domain_name in response.json()['domains']


def test_linksroute_get_positive(test_app):
    """ Тестирование получения данных из базы без параметров """
    response = test_app.get(f"/visited_links")
    assert response.status_code == 200 
    assert test_domain_name in response.json()['domains']
