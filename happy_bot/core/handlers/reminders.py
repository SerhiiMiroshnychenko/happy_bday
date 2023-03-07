from aiogram import Bot
from aiogram.types import Message
from asgiref.sync import sync_to_async

from datetime import datetime

from happy_bot.models import Profile, User
from happy_site.models import Reminder, BDays
from happy_bot.core.handlers.basic import check_user


# Отримуємо об'єкт User по його id
@sync_to_async
def get_user_for_user_id(user_id: int):
    user = None
    try:
        user = User.objects.get(id=user_id)
    except BaseException as e:
        print(e.__class__, e)
    return user


# Запит в базу даних за нагадуваннями для користувача
@sync_to_async
def get_reminders(user):
    rems = Reminder.objects.filter(user_id=user)
    print(f'{rems=}')
    reminders = []
    for rem in rems:
        birthday = BDays.objects.get(id=rem.bday_id)
        info = birthday.title, birthday.date, birthday.get_age(), rem.text, rem.date_time
        reminders.append(info)
    print(f'{reminders=}')
    return reminders


# Надсилання нагадування користувачу
async def send_reminder(bot: Bot, chat_id, reminder):
    await bot.send_message(chat_id, reminder)


# Отримання нагадувань для користувача:
async def set_reminders(message: Message, bot: Bot):
    chat_id = message.from_user.id

    user_id, user_name = await check_user(message.from_user.id)
    user = await get_user_for_user_id(user_id)
    reminders = await get_reminders(user)

    for reminder in reminders:
        # info = birthday.title, birthday.date, birthday.get_age(), rem.text, rem.date_time
        bd_title = reminder[0]
        bd_date = reminder[1]
        age = reminder[2]
        r_text = reminder[3]
        r_date = reminder[4]
        await send_reminder(
            bot, chat_id,
            f'Нагадування про День народження:\n'
            f'Іменинник: <b>{bd_title}</b>\n'
            f'Коли: <b>{bd_date.strftime("%d.%m.%Y")}</b>\n'
            f'Виповнюється: <b>{age}</b> років\n'
            f'Текст нагадування: "{r_text}"\n'
            f'Дата нагадування: {r_date.strftime("%d.%m о %H:%M")}')


# Задаємо дату, коли потрібно викликати функцію
job_date = datetime(2023, 3, 7, 10, 0, 0)


async def send_message_date(bot: Bot, chat_id: int):
    await bot.send_message(chat_id, f'Це повідомлення отримано по заданій даті:'
                                     f'{job_date}.')
