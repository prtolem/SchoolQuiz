from aiogram_dialog import DialogManager


async def get_questions(
        dialog_manager: DialogManager,
        **_,
):
    dialog_manager.dialog_data.setdefault('questions', [])
    return {'questions': dialog_manager.dialog_data.get('questions'),}


async def get_answers(
        dialog_manager: DialogManager,
        **_,
):
    dialog_manager.dialog_data['questions'][-1].setdefault('answers', [])
    return {'answers': dialog_manager.dialog_data['questions'][-1]['answers'],
            'is_answers_done': len(dialog_manager.dialog_data['questions'][-1]['answers']) < 10,
            'can_continue': len(dialog_manager.dialog_data['questions'][-1]['answers']) >= 2}
