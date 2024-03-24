from typing import Optional, Sequence

from sqlalchemy import insert, select

from src.database.models import Question
from .base import BaseRepository


class QuestionRepository(BaseRepository):
    async def get_by_id(self, question_id: int) -> Optional[Question]:
        query = select(Question).where(Question.id == question_id)
        result = await self.session.scalar(query)
        return result

    async def get_all(self) -> Sequence[Question]:
        query = select(Question)
        result = await self.session.scalars(query)
        return result.all()

    async def create(self, **values) -> Question:
        query = insert(Question).values(values).returning(Question)
        result = await self.session.scalar(query)
        await self.session.flush()
        return result

    async def update(self, question: Question) -> None:
        await self.session.merge(question)
        await self.session.flush()
