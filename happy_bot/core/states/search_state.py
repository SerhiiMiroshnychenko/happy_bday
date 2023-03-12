from aiogram.fsm.state import State, StatesGroup


class SearchState(StatesGroup):
    waiting_for_object = State()
