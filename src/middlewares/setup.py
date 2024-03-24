from aiogram import Dispatcher
from sqlalchemy.ext.asyncio import async_sessionmaker

from .database import DatabaseMiddleware


def setup_middlewares(
        dispatcher: Dispatcher, session_maker: async_sessionmaker
):
    dispatcher.update.outer_middleware(DatabaseMiddleware(session_maker))
