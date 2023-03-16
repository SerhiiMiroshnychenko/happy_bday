"""THE BOT INITIALIZATION"""
from aiogram import Bot
from happy_bday.settings import TELEGRAM_BOT_TOKEN


bot = Bot(token=TELEGRAM_BOT_TOKEN, parse_mode='HTML')
