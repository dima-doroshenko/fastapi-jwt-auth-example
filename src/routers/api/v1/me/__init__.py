from fastapi import APIRouter

router = APIRouter()

from .get import router as root_router
router.include_router(root_router)

from .delete import router as delete_router
router.include_router(delete_router)

from .edit import router as edit_router
router.include_router(edit_router)