from aiogram import Router, types
from aiogram.fsm.context import FSMContext

from src.callback_data.quiz import IntoQuizButtonCallbackData
from src.database import QuizService
from src.states.quiz import QuizState

router = Router()


@router.callback_query(IntoQuizButtonCallbackData.filter())
async def into_quiz_handler(
        call: types.CallbackQuery,
        callback_data: IntoQuizButtonCallbackData,
        state: FSMContext,
        quiz_service: QuizService
):
    quiz = await quiz_service.get_by_id(callback_data.quiz_id)
    await state.set_state(QuizState.question)
    await call.message.delete()
    await state.set_data({'question_id': 0, 'quiz_id': callback_data.quiz_id})
    await call.message.answer_poll(
        question=quiz.questions[0].question_text,
        options=[answer['answer'] for answer in quiz.questions[0].answers],
        type='quiz',
        correct_option_id=
        [i for i in range(len(quiz.questions[0].answers)) if quiz.questions[0].answers[i]['is_correct']][0],
        open_period=30,
        is_anonymous=False
    )


@router.poll_answer(QuizState.question)
async def answer_handler(
        poll_answer: types.PollAnswer,
        state: FSMContext,
        quiz_service: QuizService
):
    question_id = (await state.get_data())['question_id']
    quiz = await quiz_service.get_by_id(int((await state.get_data())['quiz_id']))
    
