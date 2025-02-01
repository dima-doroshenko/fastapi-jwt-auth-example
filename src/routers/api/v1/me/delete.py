from fastapi import APIRouter

from utils.auth import get_current_user
from schemas import Answer


router = APIRouter()


@router.delete("/", response_model_exclude_none=True)
async def deactivate_account(
    user: get_current_user,
) -> Answer:
    user.is_active = False
    return Answer()
