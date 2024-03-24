from aiogram import Router, filters, types
from aiogram.filters import CommandObject
from aiogram.utils.deep_linking import decode_payload

from src.database import QuizService
from src.keyboards.quiz import get_into_quiz_keyboard
from src.keyboards.start import get_start_keyboard
from src.database.models import History

router = Router()


def check_user_history(histories: list[History], user: types.User) -> bool:
    for history in histories:
        if history.user_id == user.id:
            return False
    return True


@router.message(filters.Command("start"))
async def cmd_start(message: types.Message, command: CommandObject, quiz_service: QuizService):
    if command.args:
        try:
            quiz_id = int(decode_payload(command.args))
        except Exception:
            await message.answer(
                'Выберите действие на клавиатуре.',
                reply_markup=get_start_keyboard()
            )
            return
        quiz = await quiz_service.get_by_id(quiz_id)
        if quiz:
            if check_user_history(quiz.histories, message.from_user):
                await message.answer('Вам доступен тест для прохождения.\n\n'
                                     'Нажмите кнопку чтобы приступить к прохождению.',
                                     reply_markup=get_into_quiz_keyboard(quiz_id))
                return
    await message.answer(
        'Выберите действие на клавиатуре.',
        reply_markup=get_start_keyboard()
    )
