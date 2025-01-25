from pydantic_settings import BaseSettings
from pydantic import BaseModel

from pathlib import Path
from datetime import timedelta

BASEDIR = Path(__file__).parent.parent


class Email(BaseModel):
    login: str = 'text@example.com'
    password: str = 'password123'
    code_expire_timedelta: timedelta = timedelta(minutes=15)

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


class Settings(BaseSettings):
    db: DBSettings = DBSettings()
    auth_jwt: AuthJwt = AuthJwt()
    auth: Auth = Auth()
    email: Email = Email()


settings = Settings()
