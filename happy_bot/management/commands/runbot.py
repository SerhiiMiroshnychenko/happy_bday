from django.core.management.base import BaseCommand

import asyncio
import logging
from happy_bday.settings import TELEGRAM_BOT_TOKEN, TIME_ZONE
from happy_bot.core.bot_dicpatcher.set_dispatcher import dp, Bot
from happy_bot.bd_bot import bot

# ПЛАНУВАЛЬНИК
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from happy_bot.core.handlers import schedul_task
from datetime import datetime, timedelta

from happy_bot.core.bot_scheduler.schedule_block import scheduler


async def start():
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - [%(levelname)s] - %(name)s - '
                               '(%(filename)s).%(funcName)s(%(lineno)d) - %(message)s'
                        )

    scheduler.start()

    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


class Command(BaseCommand):
    help = 'RUN COMMAND: python manage.py runbot'

    def handle(self, *args, **options):
        asyncio.run(start())
