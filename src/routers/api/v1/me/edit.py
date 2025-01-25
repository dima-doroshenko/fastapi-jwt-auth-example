from fastapi import APIRouter

from utils.auth import get_current_user
from schemas import Answer, UserNewUsername


router = APIRouter()


@router.patch("/", response_model_exclude_none=True)
async def edit_username(
    user: get_current_user, new_username_data: UserNewUsername
) -> Answer:
    await user.set_username(new_username_data.username)
    return Answer()
