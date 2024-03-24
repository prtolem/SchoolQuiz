from aiogram import Dispatcher
from aiogram_dialog import setup_dialogs as _setup_dialogs

from .new_quiz import quiz_dialog


def setup_dialogs(dispatcher: Dispatcher):
    dialogs = [quiz_dialog]
    dispatcher.include_routers(*dialogs)
    _setup_dialogs(dispatcher)
