"""ЗАГАЛЬНИЙ STATE ДЛЯ ПОШУКУ"""
from aiogram.fsm.state import State, StatesGroup


class SearchState(StatesGroup):
    """
    State object for searching
    """
    waiting_for_object = State()
