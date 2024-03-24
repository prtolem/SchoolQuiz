from typing import Optional, Sequence

from sqlalchemy import insert, select

from src.database.models import Quiz
from .base import BaseRepository


class QuizRepository(BaseRepository):
    async def get_by_id(self, quiz_id: int) -> Optional[Quiz]:
        query = select(Quiz).where(Quiz.id == quiz_id)
        result = await self.session.scalar(query)
        return result

    async def get_all(self) -> Sequence[Quiz]:
        query = select(Quiz)
        result = await self.session.scalars(query)
        return result.all()

    async def create(self, **values) -> Quiz:
        query = insert(Quiz).values(values).returning(Quiz)
        result = await self.session.scalar(query)
        await self.session.flush()
        return result

    async def update(self, quiz: Quiz) -> None:
        await self.session.merge(quiz)
        await self.session.flush()
