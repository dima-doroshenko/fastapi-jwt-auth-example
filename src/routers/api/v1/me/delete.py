from fastapi import APIRouter

from utils.auth import get_current_user
from schemas import Answer


router = APIRouter()


@router.delete("/", response_model_exclude_none=True)
async def delete_account(
    user: get_current_user,
) -> Answer:
    await user.delete()
    return Answer()
