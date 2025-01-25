from uuid import uuid4, UUID
from datetime import datetime

from typing import TYPE_CHECKING

from fastapi import HTTPException, status

from sqlalchemy.exc import IntegrityError
from sqlalchemy import delete

from database import EmailMessagesOrm, EmailConfirmationType
from database.annotations import now
from schemas import Answer

from .basic_dto import BasicDTO

if TYPE_CHECKING:
    from repository import User


class Email(BasicDTO):

    def __init__(self, user: "User"):
        self.crud = user.crud
        self.session = user.session
        self.user = user
        self._verifcation_code: str | None = None

    @property
    def verifcation_code(self) -> UUID:
        if self._verifcation_code is None:
            self._verifcation_code = uuid4()
        return self._verifcation_code

    async def send_confirmation(self, confirmation_type: EmailConfirmationType) -> Answer:
        from utils import email_sender

        email_sender.send_msg(
            self.user.email,
            f"Код подтверждения: {self.verifcation_code}",
        )
        obj = EmailMessagesOrm(
            user_id=self.user.id, 
            code=self.verifcation_code, 
            type=confirmation_type
        )

        try:
            self.session.add(obj)
            await self.session.flush()
        except IntegrityError:
            await self.session.rollback()
            stmt = delete(EmailMessagesOrm).where(
                EmailMessagesOrm.user_id == self.user.id
            )
            await self.session.execute(stmt)
            self.session.add(obj)

        return Answer(detail="A confirmation message sent to your email")


    async def verify(self, code: str, confirmation_type: EmailConfirmationType) -> None:
        obj = await self.session.get(EmailMessagesOrm, self.user.id)

        if (not obj) or not all(
            (
                obj.code == UUID(code),
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
