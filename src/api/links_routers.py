from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import InterfaceError
from sqlalchemy.future import select
import validators
import time

from utils.logger import log
from models.base import Links
from db.db import get_session
from utils.exceptions import RequestException
from api.params_models import LinksParam
from api.response_models import StatusResponse, LinksResponse

linksroute_post = APIRouter()
linksroute_get = APIRouter()

@linksroute_post.post('/visited_links')
async def add_links(links_list: LinksParam, 
                    session: AsyncSession = Depends(get_session)) -> StatusResponse:
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
        response = StatusResponse(links_errors).status
    except (RequestException, InterfaceError, ConnectionRefusedError) as ex:
        response = StatusResponse(ex).status
    log.info(str(response))

    return response

@linksroute_get.get("/visited_links", response_model=dict)
async def get_visited_links(time_from: str = None,
                    time_to: str = None,
                    session: AsyncSession = Depends(get_session)) -> dict:
    """ Получение списка уникальных доменов, которые посещал пользователь """

    query = select(Links).execution_options(populate_existing=True)
    if time_from and time_to:
        time_from = float(time_from)
        time_to = float(time_to)
        query = query.where(Links.created_at.between(time_from, time_to))
    query_result = await session.execute(query)
    visited_links = query_result.scalars().fetchall()
    response = LinksResponse(visited_links).response

    return response
