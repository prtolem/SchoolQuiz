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
    await state.set_data({'question_id': 0, 'quiz_id': callback_data.quiz_id, 'right_answers_id': []})
    poll = await call.message.answer_poll(
        question=quiz.questions[0].question_text,
        options=[answer['answer'] for answer in quiz.questions[0].answers],
        type='quiz',
        correct_option_id=
        [i for i in range(len(quiz.questions[0].answers)) if quiz.questions[0].answers[i]['is_correct']][0],
        open_period=30,
        is_anonymous=False
    )
    await state.update_data(
        poll=poll
    )


@router.poll_answer(QuizState.question)
async def answer_handler(
        poll_answer: types.PollAnswer,
        state: FSMContext,
        quiz_service: QuizService
):
    state_data = await state.get_data()
    question_id = state_data['question_id']
    quiz = await quiz_service.get_by_id(int(state_data['quiz_id']))
    poll: types.Message = state_data['poll']
    if quiz.questions[question_id].answers[poll_answer.option_ids[0]]['is_correct']:
        state_data.setdefault('right_answers_id', [])
        state_data['right_answers_id'].append(question_id)
        await state.update_data(
            right_answers_id=state_data['right_answers_id']
        )
    await poll.delete()
    question_id += 1
    if question_id == len(quiz.questions):
        await poll.answer(
            text="Вы успешно завершили прохождение тестирования! Ваши результаты были отправлены составителю теста."
        )
        await state.clear()
        await poll.bot.send_message(
            chat_id=quiz.author_id,
            text='Пользователь прошел ваш тест!\n'
                 f'<b>Username:</b> @{poll_answer.user.username}\n'
                 f'<b>ID:</b> <code>{poll_answer.user.id}</code>\n\n'
                 f'Результат: {len(state_data["right_answers_id"])}/{len(quiz.questions)}\n'
        )
        return
    await state.update_data({'question_id': question_id, 'quiz_id': quiz.id})
    poll = await poll.answer_poll(
        question=quiz.questions[question_id].question_text,
        options=[answer['answer'] for answer in quiz.questions[question_id].answers],
        type='quiz',
        correct_option_id=
        [i for i in range(len(quiz.questions[question_id].answers)) if quiz.questions[question_id].answers[i]['is_correct']][0],
        open_period=30,
        is_anonymous=False
    )
    await state.update_data(
        poll=poll
    )
