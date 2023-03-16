"""ОНОВЛЕННЯ НАГАДУВАНЬ"""

# Базові імпорти
from datetime import datetime

# Імпорти Aiogram
from aiogram import Bot
from aiogram.types import Message

from happy_bot.core.handlers.check_user import check_user, remind_about_auth
# Внутрішні імпорти
from happy_bot.core.handlers.reminders_and_birthdays import set_reminders, send_reminder_date, RInfo
from happy_bot.core.bot_scheduler.schedule_block import reminders_scheduler


async def update_reminders_for_id(bot: Bot, chat_id: int) -> None:
    """
    Оновлює нагадування по id чату.

    :param bot: Bot
    :param chat_id: int
    :return: None
    """

    reminders = await set_reminders(chat_id)
    await reminder_unpack(reminders, chat_id, bot)
    print(f'НАГАДУВАННЯ ОНОВЛЕНО {datetime.now()}')


async def update_reminders_for_message(message: Message, bot: Bot) -> None:
    """
    Оновлює нагадування по id чату взятого з повідомлення.

    :param message: Message
    :param bot: Bot
    :return: None
    """

    chat_id = message.from_user.id
    if (await check_user(chat_id))[0]:
        print(f'UPDATE {datetime.now()}')
        await update_reminders_for_id(bot, chat_id)
        await message.answer('Нагадування оновлено.')
    else:
        await remind_about_auth(chat_id)


async def reminder_unpack(reminders: list[RInfo], chat_id: int, bot: Bot) -> None:
    """
    Додає оновленні нагадування в reminders_scheduler як jobs.

    :param reminders: list[Info]
    :param chat_id: int
    :param bot: Bot
    :return: None
    """

    reminders_scheduler.remove_all_jobs()
    if not reminders:
        return None
    for reminder in reminders:
        # Задаємо дату, коли потрібно викликати функцію.
        job_date = reminder.rem_time
        job_id = str(reminder.id)
        reminders_scheduler.add_job(send_reminder_date,
                                    trigger='date', run_date=job_date,
                                    kwargs={'bot': bot, 'chat_id': chat_id,
                                            'reminder': reminder}, id=job_id)
