from aiogram import Dispatcher
from aiogram import F
from aiogram.enums import ChatAction
from aiogram.filters import CommandStart

from ..handlers.basic import *
from happy_bot.core.handlers.auth_handlers import *


dp = Dispatcher()

"""Блок реєстрації handler-ов в Диспетчері"""
dp.startup.register(start_bot)
dp.shutdown.register(stop_bot)

dp.message.register(process_auth_command, Command('auth'))
dp.message.register(process_username, AuthState.waiting_for_username)
dp.message.register(process_password, AuthState.waiting_for_password)

dp.message.register(get_photo, F.photo)  # реєструємо реакцію на фото
dp.message.register(get_glory, F.text == 'Слава Україні')
dp.message.register(get_glory, F.text == 'Слава Україні!')
dp.message.register(get_start, CommandStart())

dp.message.register(get_message, F.text)
"""Кінець блока"""
