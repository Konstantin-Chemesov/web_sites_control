from fastapi import APIRouter
from api.response_models import StatusResponse

first_page_get = APIRouter()

@first_page_get.get('/')
async def first_page() -> dict:
    """ Болванка запроса для получения статуса работы приложения """

    return StatusResponse().status