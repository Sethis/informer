from aiogram.fsm.state import State, StatesGroup


class InformationSG(StatesGroup):
    menu = State()

    one_info = State()
    delete_current_info = State()

    new_info_name = State()
    new_info_text = State()


class AdminSG(StatesGroup):
    menu = State()
    link = State()
