from aiogram import Bot
from aiogram.types import Message
from asgiref.sync import sync_to_async

from datetime import datetime, date

from happy_bot.models import User
from happy_site.models import Reminder, BDays
from happy_bot.core.handlers.check_user import check_user

from typing import NamedTuple
import pytz
from happy_bday.settings import TIME_ZONE


class Info(NamedTuple):
    id: int
    title: str
    birth_date: date
    age: int
    text: str
    rem_time: datetime


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
        info = rem.id, birthday.title, birthday.date, birthday.get_age(), rem.text, rem.date_time
        reminders.append(info)
    print(f'{reminders=}')
    return reminders


# Надсилання нагадування користувачу
async def send_reminder_date(bot: Bot, chat_id: int, reminder: Info):
    message = f'Нагадування про День народження:\n' \
              f' Іменинник:  <b>{reminder.title}</b>\n' \
              f' Коли:  <b>{reminder.birth_date.strftime("%d.%m.%Y")}</b>\n' \
              f' Виповнюється:  <b>{reminder.age}</b> років\n' \
              f' Текст:  "{reminder.text}"\n' \
              f' Дата нагадування:  ' \
              f'{reminder.rem_time.astimezone(tz=pytz.timezone(TIME_ZONE)).strftime("%d.%m о %H:%M")}'
    await bot.send_message(chat_id, message)


# Отримання всіх нагадувань для користувача та повертаємо їх як список:
async def set_reminders(chat_id: int = None) -> list[Info]:
    user_id, user_name = await check_user(chat_id)
    user = await get_user_for_user_id(user_id)
    reminders = await get_reminders(user)

    information = []
    for reminder in reminders:
        info = Info(
            id=reminder[0],
            title=reminder[1],
            birth_date=reminder[2],
            age=reminder[3],
            text=reminder[4],
            rem_time=reminder[5]
        )
        information.append(info)
        # await send_reminder_date(
        #     bot, chat_id, info)

    return information


async def show_reminders(message: Message, bot: Bot):
    chat_id = message.from_user.id
    reminders = await set_reminders(chat_id)
    for reminder in reminders:
        await send_reminder_date(bot, chat_id, reminder)


async def show_reminders_for_id(id_chat: int, bot: Bot):
    reminders = await set_reminders(id_chat)
    for reminder in reminders:
        await send_reminder_date(bot, id_chat, reminder)
