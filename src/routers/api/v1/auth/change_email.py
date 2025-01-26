from fastapi import APIRouter

from utils.auth import get_current_user
from utils import EmailIsNotVerified
from database import EmailConfirmationType
from schemas import Answer, ConfirmationEmailSchema

router = APIRouter()


@router.post("/change-email", response_model_exclude_none=True)
async def change_email(user: get_current_user) -> Answer:
    if not user.verified:
        raise EmailIsNotVerified
    await user.email_actions.send_confirmation(
        EmailConfirmationType.change_email
    )
    return Answer(detail="A confirmation message sent to your email")


@router.post("/change-email/{code}", response_model_exclude_none=True)
async def set_new_email(
    data: ConfirmationEmailSchema,
    user: get_current_user,
) -> Answer:
    await user.email_actions.verify_code(data.code, EmailConfirmationType.change_email)
    await user.email_actions.clear()
    await user.set_email(data.email)
    return Answer()