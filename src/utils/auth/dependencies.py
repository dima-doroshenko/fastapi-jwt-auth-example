from typing import Annotated, TYPE_CHECKING

from fastapi import Depends

from repository import Crud

from .meta import ACCESS_TOKEN_TYPE, REFRESH_TOKEN_TYPE
from .jwt_ import get_current_token_payload, validate_token_type
from ..exc import UserNotFoundException, UserInactiveException


if TYPE_CHECKING:
    from repository import User


class UserGetterFromToken:

    def __init__(self, token_type: str):
        self.token_type = token_type

    async def __call__(
        self,
        payload: dict = Depends(get_current_token_payload),
        crud: Crud = Depends(Crud),
    ) -> 'User':
        validate_token_type(payload, self.token_type)
        user = await crud.get_user(id=payload["sub"])
        if user is None:
            raise UserNotFoundException
        if not user.is_active:
            raise UserInactiveException
        return user


get_current_user = Annotated['User', Depends(UserGetterFromToken(ACCESS_TOKEN_TYPE))]
get_current_user_for_refresh = Annotated['User', Depends(UserGetterFromToken(REFRESH_TOKEN_TYPE))]