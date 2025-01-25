from fastapi import Depends

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from database import AsyncSession, session_dependency, UsersOrm
from utils import auth, ThisUsernameIsAlreadyTaken, ThisEmailIsAlreadyTaken
from schemas import UserRegister

from .user import User


class Crud:

    def __init__(self, session: AsyncSession = Depends(session_dependency)):
        self.session = session

    async def create_user(self, registration_data: UserRegister) -> User:
        obj = UsersOrm(
            username=registration_data.username,
            hashed_password=auth.hash_password(registration_data.password),
            email=registration_data.email
        )
        self.session.add(obj)
        try:
            await self.session.flush()
        except IntegrityError as e:
            if 'users.email' in str(e):
                raise ThisEmailIsAlreadyTaken
            else:
                raise ThisUsernameIsAlreadyTaken
        return User(self, obj)

    async def get_user_by_id(self, user_id: int) -> User | None:
        obj = await self.session.get(UsersOrm, user_id)
        if obj:
            return User(self, obj)

    async def get_user_by_username(self, username: str) -> User | None:
        query = select(UsersOrm).where(UsersOrm.username == username)
        res = await self.session.execute(query)
        user_obj = res.scalars().one_or_none()

        if user_obj:
            return User(self, user_obj)
