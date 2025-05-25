from typing import Any

from aiogram_dialog import DialogManager
from dishka.integrations.aiogram import FromDishka
from dishka.integrations.aiogram_dialog import inject

from src.adapters.database.services import InformationService, UserService


@inject
async def informations_menu(
        informations: FromDishka[InformationService],
        users: FromDishka[UserService],
        **_kwargs,
) -> dict[str, Any]:

    informations = await informations.get_informations()

    current_user = await users.get_current_user()

    return {
        "information_blocks": informations,
        "is_admin": current_user.is_admin
    }


@inject
async def one_information_menu(
        informations: FromDishka[InformationService],
        users: FromDishka[UserService],
        dialog_manager: DialogManager,
        **_kwargs,
) -> dict[str, Any]:

    current_user = await users.get_current_user()

    information = await informations.get_information_by_id(
        dialog_manager.dialog_data["block_id"]
    )

    return {
        "information": information,
        "upper_information_name": information.name.upper(),
        "is_admin": current_user.is_admin
    }
