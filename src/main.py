import uvicorn
from fastapi import FastAPI, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import InterfaceError
from sqlalchemy.future import select
from pydantic import BaseModel
from urllib.parse import urlparse
import validators
import time

from utils.logger import log
from core import config
from models.base import Links
from db.db import get_session, init_db
from utils.exceptions import RequestException


class SitesRequest(BaseModel):
    links: list[str]

class GetLinks(BaseModel):
    time_from: str
    time_to: str

class JSONResponse():
    def __init__(self, exception_text: str):
        if not exception_text:
            self.status = {'status': 'ok'}
        else:
            self.status = {'status': str(exception_text)}

app = FastAPI(redoc_url=None)
log.info('Started')

@app.on_event("startup")
async def on_startup():
    await init_db()

@app.post('/visited_links')
async def add_links(links_list: SitesRequest, session: AsyncSession = Depends(get_session)):
    """ Запись в базу информации о посещенных пользователем сайтах """
    
    try:
        links_errors = []
        created_at = time.time()
        if not links_list.links:
            raise RequestException('Список ссылок пуст')
        for link in links_list.links:
            if not validators.url(link):
                links_errors.append(f'{link} - неверный формат ссылки')
            link_to_insert = Links(link=link, created_at=created_at)
            session.add(link_to_insert)
        await session.commit()
        response = JSONResponse(links_errors).status
    except (RequestException, InterfaceError, ConnectionRefusedError) as ex:
        response = JSONResponse(ex).status
    log.info(str(response))

    return response

@app.get("/songs", response_model=dict)
async def get_songs(time_from: str = None, time_to: str = None, session: AsyncSession = Depends(get_session)):
    """ Получение списка уникальных доменов, которые посещал пользователь """

    query = select(Links).execution_options(populate_existing=True)
    if time_from and time_to:
        time_from = int(time_from)
        time_to = int(time_to)
        query = query.where(Links.created_at.between(time_from, time_to))
    result = await session.execute(query)
    songs = result.scalars().fetchall()
    links_unique = set([urlparse(link_object.link).netloc for link_object in songs])

    return {"domains": links_unique, 'status': 'ok'}

if __name__ == "__main__":
    uvicorn.run(app, host=config.PROJECT_HOST, port=config.PROJECT_PORT,)