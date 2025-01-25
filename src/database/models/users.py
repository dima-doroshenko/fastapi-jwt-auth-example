from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String

from database import Base, created_at, intpk


class UsersOrm(Base):
    __tablename__ = "users"

    id: Mapped[intpk]
    username: Mapped[str] = mapped_column(String(32), unique=True)
    email: Mapped[str] = mapped_column(unique=True)
    is_active: Mapped[bool] = mapped_column(default=True)
    verified: Mapped[bool] = mapped_column(default=False)
    hashed_password: Mapped[bytes]
    created_at: Mapped[created_at]