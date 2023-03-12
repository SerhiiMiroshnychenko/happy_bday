from aiogram import Bot
from aiogram.types import Message, CallbackQuery
from asgiref.sync import sync_to_async

from datetime import datetime, date

from happy_bot.core.utils.callbackdata import Search
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


class BDinfo(NamedTuple):
    id: int
    title: str
    content: str
    photo_path: str
    birth_date: date
    age: int


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

    reminders = []
    for rem in rems:
        birthday = BDays.objects.get(id=rem.bday_id)
        info = rem.id, birthday.title, birthday.date, birthday.get_age(), rem.text, rem.date_time
        reminders.append(info)

    return reminders


# Надсилання нагадування користувачу
async def send_reminder_date(bot: Bot, chat_id: int, reminder: Info):
    message = f'Нагадую про день народження:\n\n' \
              f'<b>{reminder.title.upper()}</b>\n' \
              f'<b>{reminder.birth_date.strftime("%d.%m.%Y")}</b>\n' \
              f'Виповнюється:  <b>{reminder.age}</b> років\n\n' \
              f' Дата нагадування:  ' \
              f'{reminder.rem_time.astimezone(tz=pytz.timezone(TIME_ZONE)).strftime("%d.%m о %H:%M")}\n' \
              f'(<i>{reminder.text}</i>)'
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
    print('\n\n\n_____OK show_reminders______\n\n\n')
    chat_id = message.from_user.id
    print(f'{chat_id=}')
    reminders = await set_reminders(chat_id)
    for reminder in reminders:
        await send_reminder_date(bot, chat_id, reminder)


async def show_reminders_for_id(id_chat: int, bot: Bot):
    reminders = await set_reminders(id_chat)
    for reminder in reminders:
        await send_reminder_date(bot, id_chat, reminder)


"""BIRTHDAYS"""


async def show_birthdays_for_id(id_chat: int, bot: Bot):
    birthdays = await set_bdays(id_chat)
    for birthday in birthdays:
        await send_birthday_date(bot, id_chat, birthday)


async def set_bdays(chat_id: int = None) -> list[BDinfo]:
    user_id, user_name = await check_user(chat_id)
    user = await get_user_for_user_id(user_id)
    bdays = await get_bdays(user)

    information = []
    for bday in bdays:
        info = BDinfo(
            id=bday[0],
            title=bday[1],
            content=bday[2],
            photo_path=bday[3],
            birth_date=bday[4],
            age=bday[5])
        information.append(info)
        # await send_reminder_date(
        #     bot, chat_id, info)

    return information


@sync_to_async
def get_bdays(user):
    bdays = BDays.objects.filter(user_id=user)

    birthdays = []
    for bday in bdays:
        info = bday.id, bday.title, bday.content, bday.photo,  bday.date, bday.get_age()
        birthdays.append(info)

    return birthdays


async def send_birthday_date(bot: Bot, chat_id: int, birthday: BDinfo):
    message = f'{birthday.photo_path}\n' \
              f'<b>{birthday.title.upper()}</b>\n' \
              f'{birthday.content}\n' \
              f'<b>{birthday.birth_date.strftime("%d.%m.%Y")}</b>\n' \
              f'Виповнюється:  <b>{birthday.age}</b> років\n\n' \

    await bot.send_message(chat_id, message)
