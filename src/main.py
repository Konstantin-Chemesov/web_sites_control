from fastapi import FastAPI, Depends, Body
from pydantic import BaseModel
import uvicorn
from core import config
from models.base import Links
from db.db import get_session
from db.db import init_db
from sqlalchemy.ext.asyncio import AsyncSession
import time
from sqlalchemy.future import select
from urllib.parse import urlparse
import validators
  

class SitesRequest(BaseModel):
    links: list[str]

class GetLinks(BaseModel):
    time_from: str
    time_to: str

class RequestException(Exception):
    pass

class JSONResponse():
    def __init__(self, exception_text: str = 'ok'):
        if exception_text != 'ok':
            exception_text = exception_text.args[0]
        self.status = {'status': exception_text}


# Инициализация объекта приложения
app = FastAPI(redoc_url=None) 

@app.on_event("startup")
async def on_startup():
    await init_db()

@app.post('/visited_links')
async def add_links(links_list: SitesRequest, session: AsyncSession = Depends(get_session)):
    try:
        created_at = time.time()
        if not links_list.links:
            raise RequestException('Список ссылок пуст')
        for link in links_list.links:
            if not validators.url(link):
                raise RequestException(f'{link} - неверный формат ссылки') # сбрасывает на первой битой ссылке
            link_to_insert = Links(link=link, created_at=created_at)
            session.add(link_to_insert)
            await session.commit()
            await session.refresh(link_to_insert)
        response = JSONResponse('ok').status
    except RequestException as ex:
        response = JSONResponse(ex).status

    return response

@app.get("/songs", response_model=dict)
async def get_songs(time_from: str = '0', time_to: str = time.time(), session: AsyncSession = Depends(get_session)):
    time_from = int(time_from)
    time_to = int(time_to)
    # после обновления данных в бд выкачка из бд не обновляется
    result = await session.execute(select(Links).where(Links.created_at.between(time_from, time_to)))
    songs = result.scalars().all()
    links_unique = set([urlparse(link_object.link).netloc for link_object in songs])

    return {"domains": links_unique, 'status': 'ok'}

if __name__ == "__main__":
    uvicorn.run(app, host=config.PROJECT_HOST, port=config.PROJECT_PORT,)