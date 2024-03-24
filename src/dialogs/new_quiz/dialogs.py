from aiogram import F
from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import Select, Button, Checkbox
from aiogram_dialog.widgets.text import Const, Format

from src.dialogs.base import Paginator
from src.states.quiz import NewQuizState
from .getters import get_questions, get_answers
from .handlers import add_new_question_handler, input_new_question_handler, input_new_answer_handler, end_quiz_handler, \
    end_answers_handler, add_new_answer_handler

add_questions_window = Window(
    Const("Добавьте вопросы."),
    Paginator(
        Select(
            Format("{item[question]}"),
            items="questions",
            id="select_questions",
            item_id_getter=lambda item: item['id'],
        ),
        id="questions",
        width=1,
        height=5,
    ),
    Button(
        Const('➕Добавить вопрос'),
        id='add_question',
        on_click=add_new_question_handler,
    ),
    Button(
        Const('➡️Закончить добавление вопросов'),
        id='end_quiz',
        when=F["questions"],
        on_click=end_quiz_handler
    ),
    state=NewQuizState.questions,
    getter=get_questions,
)

add_new_question_window = Window(
    Const('Введите вопрос.'),
    MessageInput(
        func=input_new_question_handler
    ),
    state=NewQuizState.add_question
)

add_new_question_answers_window = Window(
    Const('Добавьте ответы на вопрос.'),
    Paginator(
        Select(
            Format("{item[emoji]} {item[answer]}"),
            items="answers",
            id="select_answers",
            item_id_getter=lambda item: item['id']
        ),
        id="answers",
        width=1,
        height=10,
    ),
    Button(
        Const('➕Добавить ответ'),
        id='add_answer',
        on_click=add_new_answer_handler,
        when=F["is_answers_done"]
    ),
    Button(
        Const('➡️Закончить добавление ответов'),
        id='continue',
        when=F["can_continue"],
        on_click=end_answers_handler
    ),
    state=NewQuizState.add_question_answers,
    getter=get_answers
)

add_new_question_answer_window = Window(
    Const('Введите ответ.'),
    MessageInput(
        func=input_new_answer_handler
    ),
    Checkbox(
        Const('✅Сделать правильным ответом'),
        Const('❌Сделать неправильным ответом'),
        id='is_correct',
    ),
    state=NewQuizState.add_answer
)

quiz_dialog = Dialog(
    add_questions_window,
    add_new_question_window,
    add_new_question_answers_window,
    add_new_question_answer_window
)
