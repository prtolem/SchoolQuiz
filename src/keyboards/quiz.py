from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from src.callback_data.quiz import IntoQuizButtonCallbackData


def get_into_quiz_keyboard(quiz_id: int) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text="Перейти к прохождению",
                             callback_data=IntoQuizButtonCallbackData(quiz_id=quiz_id).pack())
    )
    return builder.as_markup()
