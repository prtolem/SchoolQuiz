from typing import List

from sqlalchemy import BigInteger, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base
from .history import History
from .question import Question


class Quiz(Base):
    __tablename__ = "quiz"

    id: Mapped[int] = mapped_column(primary_key=True)
    author_id: Mapped[int] = mapped_column(BigInteger)
    title: Mapped[str] = mapped_column(Text)
    description: Mapped[str] = mapped_column(Text, nullable=True)

    histories: Mapped[List["History"]] = relationship(lazy='selectin')
    questions: Mapped[List["Question"]] = relationship(lazy='selectin')
