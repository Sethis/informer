from aiogram import Router, F
from aiogram.types import Message
from aiogram_dialog import DialogManager, StartMode, ShowMode

from src.presentation.render.keyboard import INFORMATION
from src.presentation.states import InformationSG


router = Router()


@router.message(F.text == INFORMATION)
async def start(
        _message: Message,
        dialog_manager: DialogManager
) -> None:
    await dialog_manager.start(
        InformationSG.menu,
        mode=StartMode.RESET_STACK,
        show_mode=ShowMode.SEND,
    )
    return
