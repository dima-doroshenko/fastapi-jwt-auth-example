from typing import TYPE_CHECKING

from sqlalchemy.exc import IntegrityError

from database import UsersOrm
from utils import auth, ThisUsernameIsAlreadyTaken

from .basic_dto import BasicDTO

if TYPE_CHECKING:
    from .crud import Crud


class User(BasicDTO):
    id: int
    username: str
    is_active: bool

    def __init__(self, crud: "Crud", user_obj: UsersOrm):
        self._from_orm_to_attrs(user_obj)

        self.crud = crud
        self.session = crud.session
        self.obj = user_obj

    def check_password(self, password: str) -> bool:
        return auth.check_password(
            password=password, hashed_password=self.obj.hashed_password
        )

    async def delete(self) -> None:
        await self.session.delete(self.obj)

    async def edit_username(self, new_username: str) -> None:
        try:
            self.obj.username = new_username
            await self.session.flush()
        except IntegrityError:
            raise ThisUsernameIsAlreadyTaken