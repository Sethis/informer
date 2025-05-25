from aiogram import F
from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.text import Const, Format
from aiogram_dialog.widgets.kbd import SwitchTo, Select, Group
from aiogram_dialog.widgets.input import TextInput

from src.presentation.states import InformationSG
from . import on_event, getter

dialog = Dialog(
    Window(
        Const(
            "<b>Приветствуем!</b> "
            "\nВ этом меню собрано много полезной информации, "
            "доступной по одному нажатию на неё"
            "\nХорошего Вам дня!"
        ),
        Group(
            Select(
                Format("{item.name}"),
                id="info_choice",
                item_id_getter=lambda x: x.id,
                type_factory=int,
                items="information_blocks",
                on_click=on_event.info_blocks_selected
            ),
            SwitchTo(
                Const("+"),
                id="new_info_block",
                state=InformationSG.new_info_name,
                when=F["is_admin"]
            ),
            width=2,
        ),
        state=InformationSG.menu,
        getter=getter.informations_menu
    ),
    Window(
        Format(
            "<b>{upper_information_name}</b>"
            "\n{information.text}"
        ),
        SwitchTo(
            Const("❌ Удалить"),
            id="delete_current_info",
            state=InformationSG.delete_current_info,
            when=F["is_admin"]
        ),
        SwitchTo(
            Const("< К меню"),
            state=InformationSG.menu,
            id="back"
        ),
        state=InformationSG.one_info,
        getter=getter.one_information_menu
    ),
    Window(
        Format(
            "Вы уверены,"
            " что хотите удалить информационный блок {information.name}?"
        ),
        SwitchTo(
            Const("Да, удалить"),
            id="yes",
            state=InformationSG.menu,
            on_click=on_event.delete_current_info_selected
        ),
        SwitchTo(
            Const("Нет, оставить"),
            id="no",
            state=InformationSG.one_info
        ),
        state=InformationSG.delete_current_info,
        getter=getter.one_information_menu
    ),
    Window(
        Const("Напишите название нового информационного блока:"),
        SwitchTo(
            Const("< К меню"),
            state=InformationSG.menu,
            id="back"
        ),
        TextInput(
            id="write_info_name",
            on_success=on_event.new_info_name_written
        ),
        state=InformationSG.new_info_name
    ),
    Window(
        Const(
            "Напишите текст нового информационного блока:"
            "\n\nОн может содержать <b>форматирование</b> <i>от телеграмм</i>"
        ),
        SwitchTo(
            Const("< К названию"),
            state=InformationSG.new_info_name,
            id="back"
        ),
        TextInput(
            id="write_info_text",
            on_success=on_event.new_info_text_written
        ),
        state=InformationSG.new_info_text
    ),
)
