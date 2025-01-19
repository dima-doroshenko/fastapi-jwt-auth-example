from fastapi import APIRouter

from utils.auth import get_current_user_for_refresh, create_access_token
from schemas import TokenInfo

router = APIRouter()


@router.post("/refresh", response_model_exclude_none=True)
async def refresh_token(user: get_current_user_for_refresh) -> TokenInfo:
    access_token = create_access_token(user)
    return TokenInfo(access_token=access_token)
