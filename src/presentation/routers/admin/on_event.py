from typing import Any

from aiogram.types import CallbackQuery
from aiogram.utils.deep_linking import create_start_link
from aiogram_dialog import DialogManager
from dishka.integrations.aiogram_dialog import inject
from dishka.integrations.aiogram import FromDishka

from src.adapters.database.services.user import UserService
from src.presentation.render.code import AbstractCodeRender, CodeData

@inject
async def add_new_link_to_data(
        callback: CallbackQuery,
        _widget: Any,
        dialog_manager: DialogManager,
        users: FromDishka[UserService],
        code_render: FromDishka[AbstractCodeRender]
) -> None:
    new_link = await users.get_admin_code()
    rendered = code_render.encode(
        CodeData(
            code_id=new_link.id,
            unencrypted_payload=new_link.payload
        )
    )

    deeplink = await create_start_link(
        callback.bot,
        payload=rendered
    )

    dialog_manager.dialog_data["link"] = deeplink

    await callback.answer(
        "Ссылка добавлена в чат! Она одноразовая. "
        "Вы можете отправить её человеку, "
        "которого необходимо сделать администратором",
        show_alert=True
    )
