from typing import Any

from pydantic_settings import BaseSettings
from pydantic import BaseModel

import dotenv
from pathlib import Path
from datetime import timedelta

BASEDIR = Path(__file__).parent.parent

env = dotenv.dotenv_values(str(BASEDIR / ".env"))

class Email(BaseModel):
    server: str = "smtp.gmail.com"
    port: int = 587
    login: str = env.get("EMAIL_LOGIN")
    password: str = env.get("EMAIL_PASSWORD")
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
    test_url: str = url[:-3] + "_test.db"

class App(BaseModel):
    name: str = "FastAPI JWT Auth"
    debug: bool = True

class Settings(BaseSettings):
    db: DBSettings = DBSettings()
    auth_jwt: AuthJwt = AuthJwt()
    auth: Auth = Auth()
    email: Email = Email()
    app: App = App()

    def debug_decorator(self, func):
        '''Если debug == True, функция не выполнится'''

        def wrapper(*args, **kwgs) -> Any | None:
            if not self.app.debug:
                return func(*args, **kwgs)
                
        return wrapper


settings = Settings()
