from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

from src.adapters.database.dto import UserDTO

ADMIN = "☀ Администрирование"
INFORMATION = "❓ Информация"

def get_keyboard(user: UserDTO) -> ReplyKeyboardMarkup:
    if user.is_admin:
        admin_kb = [
            [KeyboardButton(text=ADMIN), ]
        ]

    else:
        admin_kb = []

    return ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text=INFORMATION),
            ],
            *admin_kb
        ],
        resize_keyboard=True,
        is_persistent=True,
        input_field_placeholder="Удачного Вам дня!"
    )
