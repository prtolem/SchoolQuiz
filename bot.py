import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.client.bot import DefaultBotProperties

from config import Config
from src import setup_middlewares, setup_handlers, setup_dialogs
from src.database import create_session_factory


async def main():
    logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(name)s - %(message)s")

    config = Config.from_file("config.toml")

    session_maker = create_session_factory(config.database.dsn)

    dp = Dispatcher()

    setup_middlewares(dp, session_maker=session_maker)
    setup_dialogs(dp)
    setup_handlers(dp)

    bot = Bot(config.telegram.bot_token, default=DefaultBotProperties(parse_mode='HTML'))

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
