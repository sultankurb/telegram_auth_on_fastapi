from sqlalchemy import BigInteger, String
from sqlalchemy.orm import Mapped, mapped_column

from src.infrastructure.database.models.base import Base


class Profile(Base):
    __tablename__ = "profile"
    username: Mapped[str] = mapped_column(String, nullable=True)
    telegram_id: Mapped[int] = mapped_column(BigInteger, unique=True)
    first_name: Mapped[str] = mapped_column(String)
    photo_url: Mapped[str] = mapped_column(String, nullable=True)
