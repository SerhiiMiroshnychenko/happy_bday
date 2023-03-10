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

# @receiver(post_save, sender=Message)
# def send_new_message_notification(sender, **kwargs):
#     message = kwargs['instance']
#     partner = message.thread.participants.exclude(id=message.sender.id)[0]
#     if not message.notification:
#         send_new_message_push_notification(sender_id=message.sender.id,
#                                            recipient_id=partner.id,
#                                            content=message.text,
#                                            badge=unread(partner),
#                                            data={'id': message.id,
#                                                  'text': message.text,
#                                                  'sender': message.sender.id,
#                                                  'chat_id': message.thread.id})
#         message.notification = True
#         message.save()


async def send_message_glory(bot: Bot, chat_id: int):
    await bot.send_message(chat_id, 'Слава Нації!')


async def send_message_chat_gpt(message: Message):
    await message.answer('\U0001F916 \n\nЯ звісно не ChatGPT, але спробую допомогти)')
