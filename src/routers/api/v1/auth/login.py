from fastapi import APIRouter, Depends, Form

from utils import auth
from utils.exc import UnauthedException, UserInactiveException
from schemas import TokenInfo
from repository import Crud, User


router = APIRouter()


async def validate_auth_user(
    username: str = Form(), password: str = Form(), crud: Crud = Depends(Crud)
):
    if not (user := await crud.get_user_by_username(username)):
        raise UnauthedException
    if not user.check_password(password):
        raise UnauthedException
    if not user.is_active:
        raise UserInactiveException

    return user


@router.post("/login")
async def login(user: User = Depends(validate_auth_user)) -> TokenInfo:
    jwt_payload = {"sub": user.id, "username": user.username}
    token = auth.encode_jwt(jwt_payload)
    return TokenInfo(access_token=token, token_type="Bearer")
