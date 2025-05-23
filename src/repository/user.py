from typing import TYPE_CHECKING

from sqlalchemy.exc import IntegrityError

from database import UsersOrm
from utils import auth, ThisUsernameIsAlreadyTaken, ThisEmailIsAlreadyTaken

from .abstractions import AbstractDTO
from .properies import UserProperties
from .email import Email

if TYPE_CHECKING:
    from .crud import Crud


class User(AbstractDTO, UserProperties):

    def __init__(self, crud: "Crud", user_obj: UsersOrm):
        self.crud = crud
        self.session = crud.session
        self.obj = user_obj
        self.email_actions = Email(self)

    def check_password(self, password: str) -> bool:
        return auth.check_password(
            password=password, hashed_password=self.obj.hashed_password
        )

    async def set_username(self, username: str) -> None:
        try:
            self.obj.username = username
            await self.session.flush()
        except IntegrityError:
            raise ThisUsernameIsAlreadyTaken

    async def set_email(self, email: str) -> None:
        try:
            self.obj.email = email
            self.verified = False
            await self.session.flush()
        except IntegrityError:
            raise ThisEmailIsAlreadyTaken

    async def set_password(self, password: str) -> None:
        self.obj.hashed_password = auth.hash_password(password)
