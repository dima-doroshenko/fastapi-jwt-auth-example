from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String

from database import Base, created_at, intpk


class UsersOrm(Base):
    __tablename__ = "users"

    id: Mapped[intpk]
    username: Mapped[str] = mapped_column(String(32), unique=True)
    hashed_password: Mapped[bytes]
    is_active: Mapped[bool] = mapped_column(default=True)
    created_at: Mapped[created_at]
