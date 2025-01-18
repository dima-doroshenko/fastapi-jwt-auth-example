from fastapi import APIRouter

router = APIRouter()

from .register import router as register_router

router.include_router(
    register_router,
)

from .login import router as login_router

router.include_router(
    login_router,
)

from .logout import router as logout_router

router.include_router(
    logout_router,
)
