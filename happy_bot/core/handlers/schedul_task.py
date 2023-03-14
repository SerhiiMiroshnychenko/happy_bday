from aiogram import Bot
from aiogram.types import Message

from happy_bday.settings import ADMIN_ID
from datetime import datetime


now = datetime.now()

# Задаємо дату, коли потрібно викликати функцію
job_date = datetime(2023, 3, 6, 11, 44, 0)


async def send_message_time(bot: Bot):
    await bot.send_message(
        ADMIN_ID, 'Це повідомлення отримано через 5 сек після запуску бота.'
    )


async def send_message_cron(bot: Bot):
    await bot.send_message(ADMIN_ID, f'Це повідомлення відправляється '
                                     f'кожен день у визначений час o {now}.')


async def send_message_interval(bot: Bot):
    await bot.send_message(ADMIN_ID, 'Це повідомлення відправляється з інтервалом в 10 хв.')


async def send_message_date(bot: Bot):
    await bot.send_message(ADMIN_ID, f'Це повідомлення отримано по заданій даті:'
                                     f'{job_date}.')


async def send_message_glory(bot: Bot, chat_id: int):
    await bot.send_message(chat_id, 'Слава Нації!')


async def send_message_chat_gpt(message: Message):
    await message.answer('\U0001F916 \n\nЯ, звісно, не ChatGPT, але спробую допомогти)')
