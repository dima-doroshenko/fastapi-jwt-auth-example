from fastapi import APIRouter, Depends

from repository import Crud
from schemas import TokenInfo, UserRegister

from .login import login

router = APIRouter()


@router.post("/register")
async def register(
    registration_data: UserRegister,
    crud: Crud = Depends(Crud),
) -> TokenInfo:
    user = await crud.create_user(registration_data)
    return await login(user)
