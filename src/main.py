import sys
sys.path[0] += "/src/"

from fastapi import FastAPI

from database import engine, Base
from routers import router
from config import settings


async def app_lifespan(_: FastAPI):
    async with engine.connect() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield


app = FastAPI(
    title=settings.app.name, 
    debug=settings.app.debug,
    lifespan=app_lifespan
)
app.include_router(router)
