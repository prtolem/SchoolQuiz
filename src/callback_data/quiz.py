from aiogram.filters.callback_data import CallbackData


class IntoQuizButtonCallbackData(CallbackData, prefix="into_quiz"):
    quiz_id: int