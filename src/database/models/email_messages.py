from datetime import datetime, timedelta
from uuid import UUID

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import ForeignKey

from database import Base, created_at
from config import settings

from ..annotations import now
from ..enums import EmailConfirmationType


class EmailMessagesOrm(Base):
    __tablename__ = "email_messages"

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete='CASCADE'), primary_key=True)
    created_at: Mapped[created_at]
    expired_at: Mapped[datetime] = mapped_column(default=lambda: now() + settings.email.code_expire_timedelta)
    code: Mapped[UUID]
    type: Mapped[EmailConfirmationType]