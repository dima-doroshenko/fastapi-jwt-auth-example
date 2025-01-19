from fastapi import APIRouter, Depends, Form

from utils.auth import get_current_user
from schemas import Answer
from config import settings


router = APIRouter()

@router.patch("/", response_model_exclude_none=True)
async def edit_username(
    user: get_current_user,
    new_username: str = settings.forms.username()
) -> Answer:
    user.obj.username = new_username
    await user.session.commit()
    return Answer()