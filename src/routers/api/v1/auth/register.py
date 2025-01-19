from fastapi import APIRouter, Depends, Form

from repository import Crud
from schemas import TokenInfo

from .login import login

router = APIRouter()


@router.post("/register")
async def register(
    username: str = Form(), 
    password: str = Form(), 
    crud: Crud = Depends(Crud)
) -> TokenInfo:
    user = await crud.create_user(username, password)
    return await login(user)
