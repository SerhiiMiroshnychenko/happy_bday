from aiogram import Bot
from django.utils import timezone

from happy_bday.settings import ADMIN_ID
from datetime import datetime

now = datetime.now()
tz_now = timezone.now()

# Задаємо дату, коли потрібно викликати функцію
job_date = datetime(2023, 3, 6, 11, 44, 0)


async def send_message_time(bot: Bot):
    await bot.send_message(ADMIN_ID, f'Це повідомлення отримано через'
                                     f' 5 сек після запуску бота o {now}({tz_now}).')


async def send_message_cron(bot: Bot):
    await bot.send_message(ADMIN_ID, f'Це повідомлення відправляється '
                                     f'кожен день у визначений час o {now}({tz_now}).')


async def send_message_interval(bot: Bot):
    await bot.send_message(ADMIN_ID, f'Це повідомлення відправляється з інтервалом в 1 хв. Зараз {now}({tz_now}).')


async def send_message_date(bot: Bot):
    await bot.send_message(ADMIN_ID, f'Це повідомлення отримано по заданій даті:'
                                     f'{job_date=} => {now=}({tz_now=}).')


async def send_message_glory(bot: Bot, chat_id: int):
    await bot.send_message(chat_id, 'Слава Нації!')

