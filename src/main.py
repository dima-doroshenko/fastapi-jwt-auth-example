import sys

sys.path[0] += "/src/"

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse

from database import engine, Base
from routers import router
from schemas import Error
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


@app.exception_handler(HTTPException)
async def handle_httpexception(request: Request, exc: HTTPException):
    return JSONResponse(
        Error(
            ok=False, 
            error=exc.status_code, 
            detail=exc.detail
        ).model_dump(),
        status_code=exc.status_code
    )


app.include_router(router)
