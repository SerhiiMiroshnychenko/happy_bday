"""STATE ДЛЯ ПОШУКУ ЗА ІМ'ЯМ"""
from aiogram.fsm.state import State, StatesGroup


class SearchNameState(StatesGroup):
    """
    State object for searching by name
    """
    search_object = State()
    waiting_for_name = State()
