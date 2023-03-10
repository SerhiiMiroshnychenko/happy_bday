from aiogram import Dispatcher
from aiogram import F
from aiogram.filters import CommandStart, Command

from happy_bot.core.handlers.basic_keyboard_handlers import get_rem
from happy_bot.core.states.auth_state import AuthState

from happy_bot.core.handlers.basic import\
    start_bot, stop_bot, get_photo, get_glory,\
    get_glory_answer, get_message
from happy_bot.core.handlers.auth_handlers import process_auth_command, process_username, process_password
from happy_bot.core.handlers.basic_command_handlers import get_start, get_help, disabling_authentication
from happy_bot.core.handlers.reminders import set_reminders, show_reminders

# Middleware
from happy_bot.core.middlewares.schedul_middleware import SchedulerMiddleware
from happy_bot.core.bot_scheduler.add_reminders import make_reminders
from happy_bot.core.bot_scheduler.schedule_block import scheduler

from happy_bot.core.handlers.inline_handlers import get_macbook
from happy_bot.core.utils.callbackdata import MacInfo
from happy_bot.core.handlers.callback import select_answer, select_reminders
from happy_bot.core.handlers.callback import select_macbook

dp = Dispatcher()

"""Блок реєстрації handler-ов в Диспетчері"""
dp.update.middleware.register(SchedulerMiddleware(scheduler))  # Реєстрація
# middleware на всі типи апдейтів

dp.startup.register(start_bot)
dp.shutdown.register(stop_bot)

# dp.callback_query.register(select_macbook, F.data.startswith('apple_'))
dp.callback_query.register(select_macbook, MacInfo.filter(F.model == 'pro'))  # З таким фільтром буде реагувати
# тільки при виборі моделі 'pro'
dp.callback_query.register(select_answer, F.data.startswith(' ...'))  # додав фільтр, що не обробляло
# select_macbook, які відсікаються їхнім фільтром
dp.callback_query.register(select_reminders, F.data.startswith('show_reminders'))

dp.message.register(get_macbook, Command(commands='macbook'))

dp.message.register(process_auth_command, Command('auth'))
dp.message.register(process_username, AuthState.waiting_for_username)
dp.message.register(process_password, AuthState.waiting_for_password)

dp.message.register(get_photo, F.photo)  # реєструємо реакцію на фото

dp.message.register(get_glory, F.text == 'Слава Україні')
dp.message.register(get_glory, F.text == 'Слава Україні!')

dp.message.register(get_glory_answer, F.text == 'Смерть ворогам')
dp.message.register(get_glory_answer, F.text == 'Смерть ворогам.')
dp.message.register(get_glory_answer, F.text == 'Смерть ворогам!')
dp.message.register(get_glory_answer, F.text == 'смерть ворогам')
dp.message.register(get_glory_answer, F.text == 'смерть ворогам.')
dp.message.register(get_glory_answer, F.text == 'смерть ворогам!')

dp.message.register(get_start, CommandStart())
dp.message.register(get_help, Command('help'))

dp.message.register(set_reminders, F.text == '/rem')
dp.message.register(make_reminders, F.text == 'Оновити')
dp.message.register(get_rem, F.text == 'Нагадування')
dp.message.register(show_reminders, F.text == '/show')
dp.message.register(disabling_authentication, F.text == '/off')

dp.message.register(get_message, F.text)
"""Кінець блока"""
