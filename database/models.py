"""Database models."""

from sqlalchemy.orm import Mapped, mapped_column
from database.base import Base


class Users(Base):
    """User model."""
    __tablename__ = 'users'
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(nullable=False)
    tg_id: Mapped[int] = mapped_column(nullable=False)
    vless_uuid: Mapped[str] = mapped_column(nullable=True)
    vless_link: Mapped[str] = mapped_column(nullable=True)