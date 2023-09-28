import pytest
from httpx import AsyncClient
import asyncio



from main import app




@pytest.mark.anyio
async def test_work_positive():
    """ Тестирование работоспособности сервера """
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/")
    assert response.status_code == 200

@pytest.mark.anyio
async def test_root():
    """ Тестирование работоспособности сервера """
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/")
    assert response.status_code == 200

if __name__ == '__main__':
    ioloop = asyncio.get_event_loop()
    tasks = [test_root]
    wait_tasks = asyncio.wait(test_root())
    ioloop.run_until_complete(test_root())
    ioloop.close()