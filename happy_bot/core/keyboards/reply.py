from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, KeyboardButtonPollType
from aiogram.utils.keyboard import ReplyKeyboardBuilder

# ReplyKeyboardMarkup - для створення клавіатури
# KeyboardButton - для створення кнопки
# KeyboardButtonPollType - для створення опитувань чи вікторин


def get_reply_keyboard():
    """
    Функція для формування текстової клавіатури
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
