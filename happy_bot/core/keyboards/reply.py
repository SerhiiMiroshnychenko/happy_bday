"""ФОРМУВАННЯ REPLY КЛАВІАТУРИ"""
from aiogram.types import ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder


# Функція для формування текстової клавіатури
def get_reply_keyboard() -> ReplyKeyboardMarkup:
    """
    The get_reply_keyboard function creates a ReplyKeyboardMarkup object with the following buttons:
        - Нагадування
        - Д.Народження
        - Оновити
        - Незабаром

    :return: The ReplyKeyboardMarkup object
    """
    keyboard_builder = ReplyKeyboardBuilder()

    keyboard_builder.button(text='Нагадування')
    keyboard_builder.button(text='Д.Народження')
    keyboard_builder.button(text='Оновити')
    keyboard_builder.button(text='Незабаром')
    keyboard_builder.button(text='Слава Україні!')

    # За допомогою методу adjust визначимо скільки кнопок буде в кожному ряду (перший 2, другий 2, третій 1)
    keyboard_builder.adjust(2, 2, 1)

    return keyboard_builder.as_markup()
