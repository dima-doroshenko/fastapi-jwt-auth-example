from typing import TYPE_CHECKING, Union

from database import AsyncSession

if TYPE_CHECKING:
    from .crud import Crud
    from .user import User


class BasicDTO:
    crud: 'Crud'
    session: AsyncSession
    user: Union["User", None] = None