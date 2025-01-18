from fastapi import APIRouter

from utils import get_current_user
from schemas import UserRead

router = APIRouter()


@router.get("/")
async def get_me(user: get_current_user) -> UserRead:
    return user.obj.as_dict()
