import uvicorn
from fastapi import FastAPI
from api import links_routers, common_routers
from db.db import init_db
from core import config
from utils.logger import log

app = FastAPI(redoc_url=None)


@app.on_event("startup")
async def on_startup():
    log.info(f'server Started')
    await init_db()

@app.on_event("shutdown")
async def shutdown_event():
   log.info(f'server Shutdown')

app.include_router(common_routers.first_page_get, tags=["Common"])
app.include_router(links_routers.linksroute_get, tags=["Links"])
app.include_router(links_routers.linksroute_post, tags=["Links"])


if __name__ == "__main__":
    uvicorn.run(app, host=config.PROJECT_HOST, port=config.PROJECT_PORT,)