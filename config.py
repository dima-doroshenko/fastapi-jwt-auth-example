from typing import Callable, TypeAlias

from pydantic_settings import BaseSettings
from pydantic import BaseModel

from fastapi import Form

from pathlib import Path

BASEDIR = Path(__file__).parent

get_form_alias: TypeAlias = Callable[[], Form]

class AuthJwt(BaseModel):
    private_key_path: Path = BASEDIR / "certs" / "jwt-private.pem"
    public_key_path: Path = BASEDIR / "certs" / "jwt-public.pem"
    algorithm: str = "RS256"
    access_token_expire_minutes: int = 15
    refresh_token_expire_days: int = 30


class Auth(BaseModel):
    token_url: str = "/api/v1/auth/login"


class DBSettings(BaseModel):
    url: str = "sqlite+aiosqlite:///database.db"


class Forms(BaseModel):
    username: get_form_alias = lambda: Form(
        min_length=3,
        max_length=20,
        regex=r"^[a-zA-Z0-9_]+$",
    )
    password: get_form_alias = lambda: Form(
        min_length=8,
        regex=r"^[A-Za-z\d@$!%*?&]{8,}$",
    )


class Settings(BaseSettings):
    db: DBSettings = DBSettings()
    auth_jwt: AuthJwt = AuthJwt()
    auth: Auth = Auth()
    forms: Forms = Forms()


settings = Settings()
