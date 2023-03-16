"""DISPATCHER"""

# Імпорти Aiogram
from aiogram import Dispatcher, F
from aiogram.filters import CommandStart, Command

# Внутрішні імпорти
from happy_bot.core.handlers.basic import start_bot, stop_bot, get_glory, get_glory_answer, get_message, get_all
from happy_bot.core.handlers.basic_keyboard_handlers\
    import get_reminders_birthdays, show_month_ver, ask_name, process_name
from happy_bot.core.handlers.auth_handlers import process_auth_command, process_username, process_password
from happy_bot.core.handlers.basic_command_handlers import get_start, get_help, disabling_authentication
from happy_bot.core.handlers.reminders import show_soon_birthdays
from happy_bot.core.handlers.callback import select_reminder_birthday, select_months, select_answer
from happy_bot.core.states.auth_state import AuthState
from happy_bot.core.states.rem_name_state import RemNameState
from happy_bot.core.utils.callbackdata import Search
from happy_bot.core.middlewares.schedul_middleware import SchedulerMiddleware
from happy_bot.core.bot_scheduler.update_reminders import update_reminders_for_message
from happy_bot.core.bot_scheduler.schedule_block import scheduler

dp = Dispatcher()

"""Блок реєстрації handler-ов в Диспетчері"""
dp.update.middleware.register(SchedulerMiddleware(scheduler))  # Реєстрація middleware на всі типи апдейтів

# Пуск та зупинка бота
dp.startup.register(start_bot)
dp.shutdown.register(stop_bot)

# Основні команди
dp.message.register(get_start, CommandStart())
dp.message.register(get_help, Command('help'))
dp.message.register(process_auth_command, Command('auth'))
dp.message.register(disabling_authentication, Command('off'))

# Основна клавіатура
dp.message.register(get_reminders_birthdays, F.text == 'Нагадування')
dp.message.register(get_reminders_birthdays, F.text == 'Д.Народження')
dp.message.register(update_reminders_for_message, F.text == 'Оновити')
dp.message.register(show_soon_birthdays, F.text == 'Незабаром')

# Реєструємо реакції на callback_query
dp.callback_query.register(show_month_ver, Search.filter(F.search_function == 'show_month_ver'))
dp.callback_query.register(ask_name, Search.filter(F.search_function == 'ask_name'))
dp.callback_query.register(select_reminder_birthday, Search.filter(F.search_function == 'show_rem_bd'))
dp.callback_query.register(select_months, F.data.startswith('showmonths'))
dp.callback_query.register(ask_name, F.data == 'ask_name')
dp.callback_query.register(select_answer, F.data.startswith(' ...'))

# States
dp.message.register(process_name, RemNameState.waiting_for_name)
dp.message.register(process_username, AuthState.waiting_for_username)
dp.message.register(process_password, AuthState.waiting_for_password)

# Квест
dp.message.register(get_glory, F.text == 'Слава Україні')
dp.message.register(get_glory, F.text == 'Слава Україні!')
dp.message.register(get_glory_answer, F.text == 'Смерть ворогам')
dp.message.register(get_glory_answer, F.text == 'Смерть ворогам.')
dp.message.register(get_glory_answer, F.text == 'Смерть ворогам!')
dp.message.register(get_glory_answer, F.text == 'смерть ворогам')
dp.message.register(get_glory_answer, F.text == 'смерть ворогам.')
dp.message.register(get_glory_answer, F.text == 'смерть ворогам!')

# Відповідь на повідомлення
dp.message.register(get_message, F.text)
dp.message.register(get_all)
"""Кінець блока"""

