# from fastapi import Depends

# from repository import User, Crud

# from .meta import ACCESS_TOKEN_TYPE, REFRESH_TOKEN_TYPE
# from .jwt_ import get_current_token_payload, validate_token_type
# from ..exc import UserNotFoundException

# class UserGetterFromToken:

#     def __init__(
#         self,
#         token_type: str
#     ):
#         self.token_type = token_type

#     async def __call__(
#         self,
#         payload: dict = Depends(get_current_token_payload),
#         crud: Crud = Depends(Crud)
#     ) -> User:
#         validate_token_type(payload, self.token_type)
#         user = await crud.get_user_by_id(payload['sub'])
#         if user is None:
#             raise UserNotFoundException
#         return user

# get_current_user = UserGetterFromToken(ACCESS_TOKEN_TYPE)
# get_current_user_for_refresh = UserGetterFromToken(REFRESH_TOKEN_TYPE)
from jwt import InvalidTokenError, ExpiredSignatureError
from typing import Annotated

from fastapi import Depends

from utils.exc import (
    TokenExpiredException,
    InvalidTokenException,
    UserInactiveException,
)
from repository import User, Crud

from .meta import oauth2_scheme
from .jwt_ import decode_jwt


async def get_current_token_payload(
    token: str = Depends(oauth2_scheme),
) -> dict[str]:
    try:
        payload = decode_jwt(token)
    except ExpiredSignatureError:
        raise TokenExpiredException
    except InvalidTokenError:
        raise InvalidTokenException
    return payload


async def _get_current_user(
    payload: dict = Depends(get_current_token_payload), crud: Crud = Depends(Crud)
):
    user_id = payload.get("sub")
    if user := await crud.get_user_by_id(user_id):
        return user
    raise InvalidTokenException


async def _get_current_active_user(user: User = Depends(_get_current_user)):
    if user.is_active:
        return user
    raise UserInactiveException


get_current_user = Annotated[User, Depends(_get_current_user)]
get_current_active_user = Annotated[User, Depends(_get_current_active_user)]
