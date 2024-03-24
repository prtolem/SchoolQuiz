import logging

from aiogram.types import CallbackQuery, Message
from aiogram.utils.deep_linking import create_start_link
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import Button

from src.database import QuizService, QuestionService
from src.states.quiz import NewQuizState

logger = logging.getLogger(__name__)


async def add_new_question_handler(
        call: CallbackQuery,
        button: Button,
        manager: DialogManager,
):
    await manager.switch_to(
        NewQuizState.add_question
    )


async def add_new_answer_handler(
        call: CallbackQuery,
        button: Button,
        manager: DialogManager
):
    await manager.switch_to(
        NewQuizState.add_answer
    )


async def end_quiz_handler(
        call: CallbackQuery,
        button: Button,
        manager: DialogManager
):
    quiz_service: QuizService = manager.middleware_data['quiz_service']
    question_service: QuestionService = manager.middleware_data['question_service']
    quiz = await quiz_service.create(
        call.from_user.id,
        manager.start_data['title'],
        manager.start_data['description']
    )
    for i in range(len(manager.dialog_data['questions'])):
        question = manager.dialog_data['questions'][i]
        await question_service.create(
            quiz.id,
            question_number=i,
            question_text=question['question'],
            answers=question['answers']
        )
    await manager.done()
    await call.message.edit_text("Квиз был успешно создан!\n\n"
                                 "Ссылка для прохождения:\n"
                                 f"{await create_start_link(call.bot, quiz.id, encode=True)}")


async def end_answers_handler(
        call: CallbackQuery,
        button: Button,
        manager: DialogManager
):
    await manager.switch_to(NewQuizState.questions)


async def input_new_question_handler(
        message: Message,
        message_input: MessageInput,
        manager: DialogManager,
):
    manager.dialog_data['questions'].append({
        'question': message.text,
        'id': len(manager.dialog_data['questions'])
    })
    await manager.switch_to(NewQuizState.add_question_answers)


async def input_new_answer_handler(
        message: Message,
        message_input: MessageInput,
        manager: DialogManager,
):
    manager.dialog_data['questions'][-1]['answers'].append({
        'answer': message.text,
        'is_correct': manager.current_context().widget_data['is_correct'],
        'emoji': '✅' if manager.current_context().widget_data['is_correct'] else '❌',
        'id': len(manager.dialog_data['questions'][-1]['answers'])
    })
    await manager.switch_to(NewQuizState.add_question_answers)
