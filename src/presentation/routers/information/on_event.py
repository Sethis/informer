from typing import Any

from aiogram.types import CallbackQuery, Message
from aiogram_dialog import DialogManager
from dishka.integrations.aiogram_dialog import inject
from dishka.integrations.aiogram import FromDishka

from src.adapters.database.services import InformationService
from src.adapters.database.dto import InformationRequestDTO
from src.presentation.states import InformationSG


async def info_blocks_selected(
        _callback: CallbackQuery,
        _widget: Any,
        dialog_manager: DialogManager,
        selected_info_block_id: int
) -> None:

    dialog_manager.dialog_data["block_id"] = selected_info_block_id

    await dialog_manager.switch_to(InformationSG.one_info)


async def new_info_name_written(
        _message: Message,
        _widget: Any,
        dialog_manager: DialogManager,
        new_name: str
) -> None:

    dialog_manager.dialog_data["new_info_name"] = new_name

    await dialog_manager.switch_to(InformationSG.new_info_text)


@inject
async def new_info_text_written(
        message: Message,
        _widget: Any,
        dialog_manager: DialogManager,
        _new_text: str,
        informations: FromDishka[InformationService]
) -> None:

    await informations.insert_information(
        InformationRequestDTO(
            name=dialog_manager.dialog_data["new_info_name"],
            text=message.html_text
        )
    )

    await message.answer(
        "Новый информационный блок был успешно добавлен для всех пользователей!"
    )

    await dialog_manager.switch_to(InformationSG.menu)


@inject
async def delete_current_info_selected(
        _callback: CallbackQuery,
        _widget: Any,
        dialog_manager: DialogManager,
        informations: FromDishka[InformationService]
) -> None:

    current_info_id: int = dialog_manager.dialog_data["block_id"]

    await informations.delete_information(current_info_id)
