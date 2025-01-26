from fastapi import APIRouter, HTTPException, status

from utils.auth import get_current_user
from database import EmailConfirmationType
from schemas import Answer

router = APIRouter()


@router.post("/verify", response_model_exclude_none=True)
async def verify_email(user: get_current_user) -> Answer:
    if user.verified:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Email already verified"
        )
    await user.email_actions.send_confirmation(EmailConfirmationType.verify)
    return Answer(detail="A confirmation message sent to your email")


@router.post("/verify/{code}", response_model_exclude_none=True)
async def confirm_verification(code: int, user: get_current_user) -> Answer:
    await user.email_actions.verify_code(code, EmailConfirmationType.verify)
    await user.email_actions.clear()
    user.verified = True
    return Answer()
