from database import EmailMessagesOrm
from repository import Crud, User

from conftest import session_factory

async def verify_user():
    async with session_factory() as session:
        crud = Crud(session)
        user = await crud.get_user(id=1)
        user.verified = True
        await session.commit()

async def get_verification_code() -> int:
    async with session_factory() as session:
        obj = await session.get(EmailMessagesOrm, 1)
        return obj.code
    
async def get_me() -> User:
    async with session_factory() as session:
        crud = Crud(session)
        return await crud.get_user(id=1)