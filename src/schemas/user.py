from datetime import datetime

from pydantic import BaseModel, EmailStr, Field


class UserNewUsername(BaseModel):
    username: str = Field(
        min_length=3,
        max_length=20,
        pattern=r"^[a-zA-Z0-9_]+$",
    )

class UserNewPassword(BaseModel):
    password: str = Field(min_length=8)

class UserNewEmail(BaseModel):
    email: EmailStr


class UserLogin(UserNewUsername, UserNewPassword):
    ...


class UserRegister(UserLogin, UserNewEmail):
    ...


class UserRead(UserNewUsername, UserNewEmail):
    id: int
    verified: bool
    created_at: datetime
