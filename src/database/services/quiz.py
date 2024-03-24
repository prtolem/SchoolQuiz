import logging
from typing import Optional, Sequence

from src.database.models import Quiz
from src.database.repositories import QuizRepository

logger = logging.getLogger(__name__)


class QuizService:
    def __init__(self, repository: QuizRepository):
        self.repository = repository

    async def get_by_id(self, quiz_id: int) -> Optional[Quiz]:
        return await self.repository.get_by_id(quiz_id=quiz_id)

    async def get_all(self) -> Sequence[Quiz]:
        return await self.repository.get_all()

    async def create(self, author_id: int, title: str, description: str) -> Quiz:
        result = await self.repository.create(
            author_id=author_id,
            title=title,
            description=description
        )
        await self.repository.commit()
        logger.info(f'New record in table {Quiz.__tablename__} with id={result.id}')
        return result

    async def update(self, quiz: Quiz) -> None:
        await self.repository.update(quiz)
        await self.repository.commit()
