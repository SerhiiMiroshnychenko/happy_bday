from aiogram.filters.callback_data import CallbackData


class MacInfo(CallbackData, prefix='mac'):
    model: str
    size: int
    chip: str
    year: int
