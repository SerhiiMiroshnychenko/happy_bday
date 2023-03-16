"""ФОРМУВАННЯ INLINE КЛАВІАТУР"""
from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from happy_bot.core.utils.callbackdata import Search


def get_ukr_keyboard() -> InlineKeyboardMarkup:
    """
    The get_ukr_keyboard function returns an InlineKeyboardMarkup object for ukrainian keyboard

    :return: The InlineKeyboardMarkup object

    """
    keyboard_builder = InlineKeyboardBuilder()
    keyboard_builder.button(text='Україна', callback_data=' ...понад усе!')
    keyboard_builder.button(text='Маріуполь', callback_data=' ...це Україна!')
    keyboard_builder.button(text='Віримо', callback_data=' ...в ЗСУ!')
    keyboard_builder.button(text='Хороші руські', url='https://russianwarship.rip/')
    keyboard_builder.button(text='Супротив', url='https://t.me/mrplsprotyv')

    keyboard_builder.adjust(1, 1, 1, 2)
    return keyboard_builder.as_markup()


def get_reminders_birthdays_keyboard(user_id: int, f_object: str) -> InlineKeyboardMarkup:
    """
    The get_reminders_birthdays_keyboard function returns an InlineKeyboardMarkup object that contains
        three buttons to select a method of searching for

    :param user_id: int: Identify the user
    :param f_object: str: Determine which object to search for
    :return: A keyboard for the user to select a method of searching for
    """
    keyboard_builder = InlineKeyboardBuilder()

    keyboard_builder.button(text='За місяцем',
                            callback_data=Search(
                                search_object=f_object,
                                search_function='show_month_ver',
                                user_id=user_id
                            ))
    keyboard_builder.button(text='За іменинником', callback_data=Search(
                                search_object=f_object,
                                search_function='ask_name',
                                user_id=user_id
                            ))
    keyboard_builder.button(text='Показати всі', callback_data=Search(
                                search_object=f_object,
                                search_function='show_rem_bd',
                                user_id=user_id
                            ))

    keyboard_builder.adjust(2, 1)
    return keyboard_builder.as_markup()


month_names = {
            1: 'Січень',
            2: 'Лютий',
            3: 'Березень',
            4: 'Квітень',
            5: 'Травень',
            6: 'Червень',
            7: 'Липень',
            8: 'Серпень',
            9: 'Вересень',
            10: 'Жовтень',
            11: 'Листопад',
            12: 'Грудень'
        }


def get_months_keyboard(user_id: int, f_object: str) -> InlineKeyboardMarkup:
    """
    The get_months_keyboard function is used to create a keyboard with all the months of the year.
    It takes two arguments: user_id and f_object. The user_id argument is used to identify which
    user's data should be shown in the next step, while f_object specifies whether we are dealing with
    the 'reminders' or 'birthdays' object.

    :param user_id: int: Identify the user
    :param f_object: str: Determine whether the user wants to see his reminders or birthdays
    :return: A keyboard with the months of the year
    """
    keyboard_builder = InlineKeyboardBuilder()
    for number, month in month_names.items():
        keyboard_builder.button(text=month, callback_data=f'showmonths_{user_id}_{number}_{f_object}')

    keyboard_builder.adjust(2, 3, 3, 3, 1)
    return keyboard_builder.as_markup()
