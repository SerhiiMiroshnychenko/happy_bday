# VERSION 1
import asyncio
import logging
from datetime import datetime
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters import Command, Text
from aiogram.types import ParseMode
from django.core.management import BaseCommand
from django.conf import settings

from happy_site.models import Reminder


class BotCommand(BaseCommand):
    help = 'Telegram bot for reminders'

    def handle(self, *args, **options):
        bot = Bot(token=settings.TELEGRAM_BOT_TOKEN)
        storage = MemoryStorage()
        dp = Dispatcher(bot, storage=storage)
        logging.basicConfig(level=logging.INFO)

        async def send_reminder(bday, text):
            chat_id = bday.user.telegram_chat_id
            await bot.send_message(chat_id=chat_id, text=text)

        async def on_startup(dp):
            await bot.send_message(chat_id=settings.TELEGRAM_ADMIN_CHAT_ID, text='Bot started')

            reminders = Reminder.objects.filter(date_time__gte=datetime.now()).order_by('date_time')
            for reminder in reminders:
                text = reminder.text
                bday = reminder.bday
                dp.loop.create_task(send_reminder(bday, text))

        async def on_shutdown(dp):
            await bot.close()

        @dp.message_handler(commands=['start'])
        async def start_handler(message: types.Message):
            await message.reply('Привіт! Я бот для нагадувань про дні народження.')

        @dp.message_handler(Command('help'))
        async def help_handler(message: types.Message):
            help_text = """
            Я надсилатиму повідомлення про дні народження у вказаний час. Для цього треба:

            1. Додати день народження у базу даних на сайті.
            2. Встановити нагадування про день народження на сайті.

            І все готово! Я надсилатиму повідомлення у вказаний час.
            """
            await message.reply(help_text)

        async def scheduler():
            while True:
                reminders = Reminder.objects.filter(date_time__gte=datetime.now()).order_by('date_time')
                if not reminders:
                    await asyncio.sleep(60)
                    continue

                reminder = reminders.first()
                text = reminder.text
                bday = reminder.bday
                delay = (reminder.date_time - datetime.now()).total_seconds()
                await asyncio.sleep(delay)

                dp.loop.create_task(send_reminder(bday, text))