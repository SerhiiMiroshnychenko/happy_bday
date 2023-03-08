from aiogram import Dispatcher
from aiogram import F
from aiogram.filters import CommandStart, Command

from happy_bot.core.states.auth_state import AuthState

from happy_bot.core.handlers.basic import start_bot, stop_bot, get_photo, get_glory, get_glory_answer, get_message
from happy_bot.core.handlers.auth_handlers import process_auth_command, process_username, process_password
from happy_bot.core.handlers.basic_command_handlers import get_start, get_help
from happy_bot.core.handlers.reminders import set_reminders

# Middleware
from happy_bot.core.middlewares.schedul_middleware import SchedulerMiddleware
from happy_bot.core.bot_scheduler.add_reminders import make_reminders
from happy_bot.core.bot_scheduler.schedule_block import scheduler


dp = Dispatcher()

"""Блок реєстрації handler-ов в Диспетчері"""
dp.update.middleware.register(SchedulerMiddleware(scheduler))  # Реєстрація
# middleware на всі типи апдейтів

dp.startup.register(start_bot)
dp.shutdown.register(stop_bot)

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
dp.message.register(make_reminders, F.text == '/up')


dp.message.register(get_message, F.text)
"""Кінець блока"""
