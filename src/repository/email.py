import secrets
from datetime import datetime

from typing import TYPE_CHECKING

from fastapi import HTTPException, status

from sqlalchemy.exc import IntegrityError
from sqlalchemy import delete

from database import EmailMessagesOrm, EmailConfirmationType
from database.annotations import now

from .abstractions import AbstractDTO

if TYPE_CHECKING:
    from repository import User


class Email(AbstractDTO):

    def __init__(self, user: "User"):
        self.crud = user.crud
        self.session = user.session
        self.user = user
        self._verifcation_code: int | None = None

    @property
    def verifcation_code(self) -> int:
        if self._verifcation_code is None:
            self._verifcation_code = secrets.randbelow(900_000) + 100_000
        return self._verifcation_code

    async def send_confirmation(self, confirmation_type: EmailConfirmationType) -> None:
        from utils import email_sender

        email_sender.send_msg(
            self.user.email,
            f"Confirmation code: {self.verifcation_code}",
        )
        user_id = self.user.id
        obj = EmailMessagesOrm(
            user_id=user_id, 
            code=self.verifcation_code, 
            type=confirmation_type
        )

        try:
            self.session.add(obj)
            await self.session.flush()
        except IntegrityError:
            await self.session.rollback()
            stmt = delete(EmailMessagesOrm).where(
                EmailMessagesOrm.user_id == user_id
            )
            await self.session.execute(stmt)
            self.session.add(obj)


    async def verify_code(self, code: int, confirmation_type: EmailConfirmationType) -> None:
        obj = await self.session.get(EmailMessagesOrm, self.user.id)

        if (not obj) or not all(
            (
                obj.code == code,
                obj.expired_at > datetime.replace(now(), tzinfo=None),
                obj.type == confirmation_type,
            )
        ):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Verification code has expired or is invalid",
            )

    async def clear(self) -> None:
        stmt = delete(EmailMessagesOrm).where(EmailMessagesOrm.user_id == self.user.id)
        await self.session.execute(stmt)
