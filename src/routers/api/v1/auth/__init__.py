from fastapi import APIRouter

router = APIRouter()

from .register import router as register_router
router.include_router(register_router)

from .login import router as login_router
router.include_router(login_router)

from .refresh import router as refresh_router
router.include_router(refresh_router)

from .change_email import router as change_email_router
router.include_router(change_email_router)

from .forgot_password import router as forgot_password_router
router.include_router(forgot_password_router)

from .verify import router as verify_router
router.include_router(verify_router)