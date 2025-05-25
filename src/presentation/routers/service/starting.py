from dishka import FromDishka
from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command, CommandObject

from src.adapters.database.services import UserService
from src.adapters.database.dto import UserRequestDTO
from src.presentation.render import AbstractCodeRender
from src.presentation.render.keyboard import get_keyboard

router = Router()


@router.message(Command("start"))
async def start(
        message: Message,
        command: CommandObject,
        users: FromDishka[UserService],
        render: FromDishka[AbstractCodeRender]

) -> None:
    current_user = await users.get_user_by_tg_id(message.from_user.id)

    if not command.args:
        user = await users.insert_user(
            UserRequestDTO(
                tg_id=message.from_user.id,
                is_admin=current_user.is_admin if current_user else False
            )
        )
        await message.answer(
            "Добро пожаловать!",
            reply_markup=get_keyboard(user)
        )
        return

    code = render.decode(command.args)
    result = await users.check_admin_code(
        code_id=code.code_id,
        unenctypted_code=code.unencrypted_payload
    )

    if result:
        user = await users.insert_user(
            UserRequestDTO(
                tg_id=message.from_user.id,
                is_admin=True
            )
        )
        await message.answer(
            "Добро пожаловать!",
            reply_markup=get_keyboard(user)
        )
        return

    await message.answer("Данные из ссылки не сходятся!")
    return
