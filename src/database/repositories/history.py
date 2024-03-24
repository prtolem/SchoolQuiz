from typing import Optional, Sequence

from sqlalchemy import insert, select

from src.database.models import History
from .base import BaseRepository


class HistoryRepository(BaseRepository):
    async def get_by_id(self, history_id: int) -> Optional[History]:
        query = select(History).where(History.id == history_id)
        result = await self.session.scalar(query)
        return result

    async def get_all(self) -> Sequence[History]:
        query = select(History)
        result = await self.session.scalars(query)
        return result.all()

    async def create(self, **values) -> History:
        query = insert(History).values(values).returning(History)
        result = await self.session.scalar(query)
        await self.session.flush()
        return result

    async def update(self, question: History) -> None:
        await self.session.merge(question)
        await self.session.flush()
