from aiogram.types import Message
from aiogram import Bot
from happy_bot.core.bot_scheduler.schedule_block import scheduler

from happy_bot.core.handlers.reminders import set_reminders, send_reminder_date


async def rem_unpack(reminders, chat_id, bot):
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


async def make_reminders(message: Message, bot: Bot):
    print('START Add Reminders')

    chat_id = message.from_user.id
    reminders = await set_reminders(chat_id)

    await rem_unpack(reminders, chat_id, bot)

    await message.answer('Нагадування оновлено.')


async def make_reminders_for_id(bot: Bot, chat_id: int):
    print('START Add Reminders for ID')

    reminders = await set_reminders(chat_id)

    await rem_unpack(reminders, chat_id, bot)

    await bot.send_message(chat_id, 'Нагадування оновлено.')
