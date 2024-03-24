from aiogram import Router

from . import new_quiz
from . import start
from . import quiz

router = Router()

router.include_router(start.router)
router.include_router(new_quiz.router)
router.include_router(quiz.router)
