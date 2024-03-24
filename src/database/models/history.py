from sqlalchemy import BigInteger, ForeignKey, SmallInteger
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class History(Base):
    __tablename__ = "history"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(BigInteger)
    quiz_id: Mapped[int] = mapped_column(ForeignKey("quiz.id"))
    score: Mapped[int] = mapped_column(SmallInteger)
