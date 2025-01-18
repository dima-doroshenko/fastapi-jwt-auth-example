from fastapi import FastAPI

from database import engine, Base

from .routers import router


async def app_lifespan(_: FastAPI):
    async with engine.connect() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield


app = FastAPI(lifespan=app_lifespan)
app.include_router(router)

# jwt.exceptions.ExpiredSignatureError