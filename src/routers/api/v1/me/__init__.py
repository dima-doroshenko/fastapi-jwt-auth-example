from fastapi import APIRouter

router = APIRouter()

from .root import router as root_router
router.include_router(root_router)
