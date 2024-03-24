from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from aiogram_dialog import DialogManager

from src.keyboards.back import get_back_keyboard
from src.states import NewQuizState

router = Router()


@router.message(F.text == '📚 Создать квиз')
async def handler(message: types.Message, state: FSMContext):
    await message.answer('Отправьте название квиза.',
                         reply_markup=get_back_keyboard())
    await state.set_state(NewQuizState.title)


@router.message(NewQuizState.title)
async def handler(message: types.Message, state: FSMContext):
    await state.set_data({'title': message.text})
    await message.answer('Отправьте описание квиза.',
                         reply_markup=get_back_keyboard())
    await state.set_state(NewQuizState.description)


@router.message(NewQuizState.description)
async def handler(message: types.Message, state: FSMContext, dialog_manager: DialogManager):
    title = (await state.get_data()).get('title')
    await state.clear()
    await dialog_manager.start(
        NewQuizState.questions,
        data={
            'title': title,
            'description': message.text
        }
    )
