import asyncio

from aiogram.types import Message
from aiogram import Bot
from happy_bot.core.bot_scheduler.schedule_block import scheduler

from happy_bot.core.handlers.reminders import set_reminders, send_reminder_date, get_reminders, show_reminders_for_id
from asgiref.sync import async_to_sync
from happy_bot.core.bot_scheduler.schedule_block import scheduler


from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from happy_site.models import Reminder


async def rem_unpack(reminders, chat_id, bot):
    print("-------------------------------------------------------------------------START rem_unpack")
    for reminder in reminders:
        # Задаємо дату, коли потрібно викликати функцію
        job_date = reminder.rem_time
        job_id = str(reminder.id)

        if scheduler.get_job(job_id):

            scheduler.remove_job(job_id)

        scheduler.add_job(send_reminder_date,
                          trigger='date', run_date=job_date,
                          kwargs={'bot': bot, 'chat_id': chat_id,
                                  'reminder': reminder}, id=job_id)
    print("-------------------------------------------------------------------------END rem_unpack")


async def make_reminders(message: Message, bot: Bot):
    print('START Add Reminders')
    my_loop = asyncio.get_event_loop()

    print('\n\n', '#' * 20, '\n\n')
    print(f'{my_loop=}')
    print('\n\n', '#' * 20, '\n\n')

    chat_id = message.from_user.id
    reminders = await set_reminders(chat_id)

    await rem_unpack(reminders, chat_id, bot)

    print("-------------------------------------------------------------------------AWAIT message.answer")
    await message.answer('Нагадування оновлені.')
    print("-------------------------------------------------------------------------END message.answer")


async def make_reminders_for_id(bot: Bot, chat_id: int):
    print('START Add Reminders for ID')
    my_loop = asyncio.get_event_loop()

    print('\n\n', '#' * 20, '\n\n')
    print(f'{my_loop=}')
    print('\n\n', '#' * 20, '\n\n')




    reminders = await set_reminders(chat_id)

    await rem_unpack(reminders, chat_id, bot)

    print("-------------------------------------------------------------------------AWAIT bot.send_message")
    print('НАГАДУВАННЯ ОНОВЛЕНО.')
    # await bot.send_message(chat_id, 'Нагадування оновлено.')
    print("-------------------------------------------------------------------------END bot.send_message")

    print('\n\n', '#' * 20, '\n\n')
    print('END Add Reminders for ID')
    print('\n\n', '#' * 20, '\n\n')

    # await show_reminders_for_id(chat_id, bot)


# @async_to_sync
# async def make_reminders_from_view(bot: Bot, chat_id: int):
#     print('START Add Reminders from view')
#
#     reminders = await set_reminders(chat_id)
#
#     print('\n\n', reminders, '\n\n')
#
#     await rem_unpack(reminders, chat_id, bot)
#
#     await bot.send_message(chat_id, 'Нагадування оновлено:')
#     await show_reminders_for_id(chat_id, bot)
