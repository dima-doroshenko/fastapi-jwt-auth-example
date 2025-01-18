from fastapi import APIRouter, Depends

from utils import auth


router = APIRouter()


@router.post("/register")
async def register(): ...
