from pydantic import BaseModel, Field

from .user import UserNewPassword, UserNewEmail


class VerificationCode(BaseModel):
    code: int = Field(ge=100_000, lt=1_000_000)


class ConfirmationPasswordSchema(UserNewPassword, VerificationCode): ...


class ConfirmationEmailSchema(UserNewEmail, VerificationCode): ...
