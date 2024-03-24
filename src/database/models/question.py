from sqlalchemy import Text, JSON, SmallInteger, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class Question(Base):
    __tablename__ = "question"

    id: Mapped[int] = mapped_column(primary_key=True)
    quiz_id: Mapped[int] = mapped_column(ForeignKey("quiz.id"))
    question_number: Mapped[int] = mapped_column(SmallInteger)
    question_text: Mapped[Text] = mapped_column(Text)
    answers: Mapped[dict] = mapped_column(JSON)
    """
    answers - [
        {
            "text": "",
            "is_correct": bool 
        }
    ]
    """
