from aiogram.fsm.state import State, StatesGroup


class RemNameState(StatesGroup):
    search_object = State()
    waiting_for_name = State()
