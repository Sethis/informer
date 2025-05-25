from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.text import Const, Format
from aiogram_dialog.widgets.kbd import SwitchTo

from src.presentation.states import AdminSG
from . import on_event

dialog = Dialog(
    Window(
        Const(
            "Приветствую, <b>администратор</b>! "
            "Тут можно создавать ссылки,"
            " чтобы сделать других пользователей администраторами"
            "\n<b>Администратор может</b>: "
            "\n - Добавлять других администраторов"
            "\n - Добавлять и удалять информационные блоки"
        ),
        SwitchTo(
            Const("🔗 Новая ссылка"),
            id="new_link",
            state=AdminSG.link,
            on_click=on_event.add_new_link_to_data
        ),
        state=AdminSG.menu
    ),
    Window(
        Format("{dialog_data[link]}"),
        SwitchTo(
            Const("< Назад к меню"),
            state=AdminSG.menu,
            id="back"
        ),
        state=AdminSG.link
    )
)
