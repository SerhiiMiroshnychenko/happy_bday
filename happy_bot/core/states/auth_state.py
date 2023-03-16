"""STATE ДЛЯ АВТОРИЗАЦІЇ"""
from aiogram.fsm.state import State, StatesGroup


class AuthState(StatesGroup):
    """
    State object for authorization
    """
    waiting_for_username = State()
    waiting_for_password = State()
