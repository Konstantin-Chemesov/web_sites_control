import os
import pytest
from httpx import AsyncClient
import asyncio
import time
os.environ['TEST'] = 'true'
from main import app

test_domain_name = 'test_domain.ru'

@pytest.mark.anyio
async def test_first_page_get_positive():
    """ Тестирование работоспособности сервера """
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get("/")
    assert response.status_code == 200

@pytest.mark.anyio
async def test_linksroute_post_positive():
    """ Тестирование ендпоинта для записи новых веб-адресов в базу """
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post("/visited_links", 
                                     json={"links": [f"https://{test_domain_name}/"]})
    assert response.status_code == 200
    assert response.json() == {'status': 'ok'}

@pytest.mark.anyio
async def test_linksroute_get_positive():
    """ Тестирование работоспособности сервера """
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get(f"/visited_links?time_from={time.time()-10}&time_to={time.time()}")
    assert response.status_code == 200 
    assert test_domain_name in response.json()['domains']

# if __name__ == '__main__':
#     ioloop = asyncio.get_event_loop()
#     wait_tasks = asyncio.wait(test_linksroute_get_positive())
#     ioloop.run_until_complete(test_linksroute_get_positive())
#     ioloop.close()