from aiogram.fsm.state import State, StatesGroup


class AuthState(StatesGroup):
    waiting_for_username = State()
    waiting_for_password = State()
