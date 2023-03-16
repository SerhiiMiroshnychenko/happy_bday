"""CUSTOM CALLBACK DATA CLASSES"""
from aiogram.filters.callback_data import CallbackData


class Search(CallbackData, prefix='find'):
    """
    Class for callback data wrapper for search
    """
    search_object: str
    search_function: str
    user_id: int
