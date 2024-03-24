import logging
from typing import Optional, Sequence

from src.database.models import Question
from src.database.repositories import QuestionRepository

logger = logging.getLogger(__name__)


class QuestionService:
    def __init__(self, repository: QuestionRepository):
        self.repository = repository

    async def get_by_id(self, question_id: int) -> Optional[Question]:
        return await self.repository.get_by_id(question_id=question_id)

    async def get_all(self) -> Sequence[Question]:
        return await self.repository.get_all()

    async def create(self, quiz_id: int, question_number: int, question_text: str, answers: dict) -> Question:
        result = await self.repository.create(
            quiz_id=quiz_id,
            question_number=question_number,
            question_text=question_text,
            answers=answers
        )
        await self.repository.commit()
        logger.info(f'New record in table {Question.__tablename__} with id={result.id}')
        return result

    async def update(self, question: Question) -> None:
        await self.repository.update(question)
        await self.repository.commit()
