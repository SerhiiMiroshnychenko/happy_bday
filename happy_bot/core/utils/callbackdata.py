from aiogram.filters.callback_data import CallbackData


class MacInfo(CallbackData, prefix='mac'):
    model: str
    size: int
    chip: str
    year: int


class Search(CallbackData, prefix='find'):
    search_object: str
    search_function: str
    user_id: int
