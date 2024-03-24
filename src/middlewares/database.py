from typing import Any, Awaitable, Callable

from aiogram import BaseMiddleware
from aiogram.types import Update
from sqlalchemy.ext.asyncio import async_sessionmaker

from src.database import (
    QuizService, HistoryService, QuestionService
)
from src.database.repositories import (
    HistoryRepository, QuestionRepository, QuizRepository
)


class DatabaseMiddleware(BaseMiddleware):
    def __init__(self, session_maker: async_sessionmaker):
        self.session_maker = session_maker

    async def __call__(
            self,
            handler: Callable[[Update, dict[str, Any]], Awaitable[Any]],
            update: Update,
            data: dict[str, Any],
    ):
        async with self.session_maker() as session:
            data["quiz_service"] = QuizService(
                repository=QuizRepository(session=session),
            )
            data['question_service'] = QuestionService(
                repository=QuestionRepository(session=session),
            )
            data['history_service'] = HistoryService(
                repository=HistoryRepository(session=session),
            )
            return await handler(update, data)
