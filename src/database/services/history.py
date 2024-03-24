import logging
from typing import Optional, Sequence

from src.database.models import History
from src.database.repositories import HistoryRepository

logger = logging.getLogger(__name__)


class HistoryService:
    def __init__(self, repository: HistoryRepository):
        self.repository = repository

    async def get_by_id(self, history_id: int) -> Optional[History]:
        return await self.repository.get_by_id(history_id=history_id)

    async def get_all(self) -> Sequence[History]:
        return await self.repository.get_all()

    async def create(self, user_id: int, quiz_id: int, score: int) -> History:
        result = await self.repository.create(
            user_id=user_id,
            quiz_id=quiz_id,
            score=score
        )
        await self.repository.commit()
        logger.info(f'New record in table {History.__tablename__} with id={result.id}')
        return result

    async def update(self, question: History) -> None:
        await self.repository.update(question)
        await self.repository.commit()
