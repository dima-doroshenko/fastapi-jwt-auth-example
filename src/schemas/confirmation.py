from pydantic import BaseModel

from .user import UserNewPassword, UserNewEmail


class VerificationCode(BaseModel):
    code: str

class ConfirmationPasswordSchema(UserNewPassword, VerificationCode):
    ...

class ConfirmationEmailSchema(UserNewEmail, VerificationCode):
    ...