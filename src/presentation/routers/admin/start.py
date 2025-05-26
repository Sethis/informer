from aiogram import Router, F
from aiogram.types import Message
from aiogram_dialog import DialogManager, StartMode, ShowMode
from dishka.integrations.aiogram import FromDishka

from src.presentation.render.keyboard import ADMIN
from src.presentation.states import AdminSG
from src.adapters.database.services import UserService


router = Router()


@router.message(F.text == ADMIN)
async def start(
        message: Message,
        dialog_manager: DialogManager,
        users: FromDishka[UserService]
) -> None:
    current_user = await users.get_current_user()

    if not current_user.is_admin:
        await message.answer("Отказано в доступе")
        return

    await dialog_manager.start(
        AdminSG.menu,
        mode=StartMode.RESET_STACK,
        show_mode=ShowMode.SEND,
    )
    return
