from fastapi import APIRouter


router = APIRouter()

from .api import router as api_router

router.include_router(
    router=api_router
)