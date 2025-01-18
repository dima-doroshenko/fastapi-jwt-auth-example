from typing import TYPE_CHECKING, Union

from database import AsyncSession, Base

if TYPE_CHECKING:
    from ..crud import Crud
    from ..user import User


class BasicDTO:
    crud: "Crud"
    session: AsyncSession
    user: Union["User", None] = None

    def _from_orm_to_attrs(self, obj: Base):
        for key, value in obj.as_dict().items():
            setattr(self, key, value)
