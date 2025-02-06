from fastapi import APIRouter

from utils import EmailAlreadyVerified
from utils.auth import get_current_user
from database import EmailConfirmationType
from schemas import Answer, VerificationCodeSchema

router = APIRouter()


@router.post("/verify", response_model_exclude_none=True)
async def verify_email(user: get_current_user) -> Answer:
    if user.verified:
        raise EmailAlreadyVerified
    await user.email_actions.send_confirmation(EmailConfirmationType.verify)
    return Answer(detail="A confirmation message sent to your email")


@router.post("/verify/", response_model_exclude_none=True)
async def confirm_verification(verification_data: VerificationCodeSchema, user: get_current_user) -> Answer:
    await user.email_actions.verify_code(verification_data.code, EmailConfirmationType.verify)
    await user.email_actions.clear()
    user.verified = True
    return Answer()
