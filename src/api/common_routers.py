from fastapi import APIRouter, Request
from api.response_models import StatusResponse
from utils.logger import log

first_page_get = APIRouter()

@first_page_get.get('/')
async def first_page(request: Request) -> dict:
    """ Болванка запроса для получения статуса работы приложения """
    log.info(f'Request: {str(request.scope)}')
    response = StatusResponse().status
    log.info(f'Response: {response}')
    return response