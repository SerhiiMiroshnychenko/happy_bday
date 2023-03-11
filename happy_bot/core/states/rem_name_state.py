from aiogram.fsm.state import State, StatesGroup


class RemNameState(StatesGroup):
    waiting_for_name = State()
