from fastapi import APIRouter, Depends

from utils.auth import http_bearer

router = APIRouter(dependencies=[Depends(http_bearer)])

from .api import router as api_router
router.include_router(api_router)