from fastapi import APIRouter

from utils.auth import get_current_user
from utils import EmailIsNotVerified, text
from database import EmailConfirmationType
from schemas import Answer, ConfirmationPasswordSchema

router = APIRouter()


@router.post("/forgot-password", response_model_exclude_none=True)
async def forgot_password(user: get_current_user) -> Answer:
    if not user.verified:
        raise EmailIsNotVerified
    await user.email_actions.send_confirmation(
        EmailConfirmationType.forgot_password
    )
    return Answer(detail=text.confirmation_sent)


@router.post("/forgot-password/", response_model_exclude_none=True)
async def set_new_password(
    data: ConfirmationPasswordSchema,
    user: get_current_user,
) -> Answer:
    await user.email_actions.verify_code(data.code, EmailConfirmationType.forgot_password)
    await user.email_actions.clear()
    await user.set_password(data.password)
    return Answer()