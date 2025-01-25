import sys
sys.path[0] += "/src/"

from fastapi import FastAPI

from database import engine, Base
from routers import router


async def app_lifespan(_: FastAPI):
    async with engine.connect() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield


app = FastAPI(title="JWT Auth Example", lifespan=app_lifespan)
app.include_router(router)
