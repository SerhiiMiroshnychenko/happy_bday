from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from happy_bot.core.utils.callbackdata import MacInfo, Search


def get_ukr_keyboard():
    keyboard_builder = InlineKeyboardBuilder()
    keyboard_builder.button(text='Україна', callback_data=' ...понад усе!')
    keyboard_builder.button(text='Маріуполь', callback_data=' ...це Україна!')
    keyboard_builder.button(text='Віримо', callback_data=' ...в ЗСУ!')
    keyboard_builder.button(text='Хороші руські', url='https://russianwarship.rip/')
    keyboard_builder.button(text='Супротив', url='https://t.me/mrplsprotyv')

    keyboard_builder.adjust(1, 1, 1, 2)
    return keyboard_builder.as_markup()


def get_macbook_keyboard():
    keyboard_builder = InlineKeyboardBuilder()
    keyboard_builder.button(text='Macbook Air 13" M1 2020',
                            callback_data=MacInfo(model='air', size=13, chip='m1', year=2020))
    keyboard_builder.button(text='Macbook Pro 14" M1 Pro 2021',
                            callback_data=MacInfo(model='pro', size=14, chip='m1', year=2021))
    keyboard_builder.button(text='Apple MacBook Pro 16" 2019',
                            callback_data=MacInfo(model='pro', size=16, chip='i7', year=2019))

    keyboard_builder.adjust(1, 1, 1)
    return keyboard_builder.as_markup()


def get_rem_bd_keyboard(user_id: int, f_object: str):
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


def get_months_keyboard(user_id: int, f_object: str):
    keyboard_builder = InlineKeyboardBuilder()
    for number, month in month_names.items():
        keyboard_builder.button(text=month, callback_data=f'showmonths_{user_id}_{number}_{f_object}')

    keyboard_builder.adjust(2, 3, 3, 3, 1)
    return keyboard_builder.as_markup()

