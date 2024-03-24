from aiogram.fsm.state import State, StatesGroup


class NewQuizState(StatesGroup):
    title = State()
    description = State()
    questions = State()
    add_question = State()
    add_question_answers = State()
    add_answer = State()


class QuizState(StatesGroup):
    question = State()
