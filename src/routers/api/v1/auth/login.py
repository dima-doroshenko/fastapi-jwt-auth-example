from fastapi import APIRouter, Depends, Form

from utils import auth
from utils.exc import UnauthedException, UserInactiveException
from schemas import TokenInfo
from repository import Crud, User

router = APIRouter()


async def validate_auth_user(
    username: str = Form(),
    password: str = Form(),
    crud: Crud = Depends(Crud),
):
    filter_key = "email" if "@" in username else "username"
    if not (user := await crud.get_user(**{filter_key: username})):
        raise UnauthedException
    if not user.check_password(password):
        raise UnauthedException
    if not user.is_active:
        raise UserInactiveException

    return user


@router.post("/login", description="Login to your account via username or email")
async def login(user: User = Depends(validate_auth_user)) -> TokenInfo:
    access_token = auth.create_access_token(user)
    refresh_token = auth.create_refresh_token(user)
    return TokenInfo(access_token=access_token, refresh_token=refresh_token)
