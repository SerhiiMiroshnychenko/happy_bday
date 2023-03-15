from aiogram import Bot
from aiogram.types import Message, CallbackQuery
from asgiref.sync import sync_to_async



from happy_bot.core.handlers.birthdays_name_handlers import make_bdays_list
from happy_bot.core.handlers.send_bday_date import send_birthday_date
from happy_bot.core.utils.callbackdata import Search
from happy_bot.core.utils.named_tuple_classes import Info, BDinfo
from happy_bot.models import User
from happy_site.models import Reminder, BDays
from happy_bot.core.handlers.check_user import check_user, get_user_for_user_id


import pytz
from happy_bday.settings import TIME_ZONE

from datetime import datetime
from happy_bot.core.handlers.send_media import get_picture, get_birthday_photo






# Запит в базу даних за нагадуваннями для користувача
@sync_to_async
def get_reminders(user):
    rems = Reminder.objects.filter(user_id=user)

    now = datetime.now()

    reminders = []
    for rem in rems:

        if rem.date_time.date() < now.date():
            rem.date_time = rem.date_time.replace(year=rem.date_time.year + 1)
            rem.save()

        birthday = BDays.objects.get(id=rem.bday_id)
        info = rem.id, birthday.title, birthday.date, birthday.get_age(), rem.text, rem.date_time
        reminders.append(info)

    return reminders


# Надсилання нагадування користувачу
async def send_reminder_date(bot: Bot, chat_id: int, reminder: Info):
    reminder_dtime = reminder.rem_time.astimezone(tz=pytz.timezone(TIME_ZONE)).strftime("%d.%m.%y о %H:%M")
    message_for_user = f'Нагадую про день народження:\n\n' \
              f'<b>{reminder.title.upper()}</b>\n' \
              f'<b>{reminder.birth_date.strftime("%d.%m.%Y")}</b>\n' \
              f'Виповнюється:  <b>{reminder.age}</b> років\n\n' \
              f' Дата нагадування:  ' \
              f'{reminder_dtime}\n' \
              f'(<i>{reminder.text}</i>)'
    dtime_now = datetime.now().strftime("%d.%m.%y о %H:%M")

    if reminder_dtime == dtime_now:
        await get_picture(chat_id, bot, message_for_user, 'clock')
    else:
        await bot.send_message(chat_id, message_for_user)


# Отримання всіх нагадувань для користувача та повертаємо їх як список:
async def set_reminders(chat_id: int = None) -> list[Info]:
    user_id, user_name = await check_user(chat_id)
    user = await get_user_for_user_id(user_id)
    reminders = await get_reminders(user)

    return [
        Info(
            id=reminder[0],
            title=reminder[1],
            birth_date=reminder[2],
            age=reminder[3],
            text=reminder[4],
            rem_time=reminder[5],
        )
        for reminder in reminders
    ]


async def show_reminders(message: Message, bot: Bot):
    chat_id = message.from_user.id
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


async def set_bdays(chat_id: int = None, version: str = None) -> list[BDinfo] or tuple[list[BDinfo], list[BDinfo]]:
    user_id, user_name = await check_user(chat_id)

    user = await get_user_for_user_id(user_id)

    if version != 'soon':
        bdays = await get_bdays(user)
        t_bdays, n_bdays = None, None

    else:
        t_bdays, n_bdays = await get_soon_bdays(user)
        bdays = None

    if bdays:
        return await make_bdays_list(bdays)

    t_info = await make_bdays_list(t_bdays)
    n_info = await make_bdays_list(n_bdays)

    return t_info, n_info



@sync_to_async
def get_bdays(user):
    bdays = BDays.objects.filter(user_id=user)

    birthdays = []
    for bday in bdays:
        info = bday.id, bday.title, bday.content, bday.photo,  bday.date, bday.get_age()
        birthdays.append(info)

    return birthdays


"""SOON BIRTHDAYS"""


@sync_to_async
def get_soon_bdays(user):
    # Отримуємо сьогоднішню дату
    today = datetime.now()

    # Знаходимо сьогоднішні дні народження
    today_birthdays = BDays.objects.filter(
        date__month=today.month,
        date__day=today.day,
        user=user
    ).order_by('date', 'title')

    # Знаходимо наступні дні народження
    birthdays = BDays.objects.filter(user=user).order_by('date__month', 'date__day', 'title')

    next_day_month = None, None
    for birthday in birthdays:
        bday_month = birthday.date.month
        bday_day = birthday.date.day
        if (
                bday_month == today.month
                and bday_day > today.day
                or bday_month != today.month
                and bday_month > today.month
        ):
            next_day_month = birthday.date.day, birthday.date.month
            break

    next_birthdays = BDays.objects.filter(
        date__month=next_day_month[1],
        date__day=next_day_month[0],
        user=user
    ).order_by('date', 'title')

    today_bdays = []
    for bday in today_birthdays:
        info = bday.id, bday.title, bday.content, bday.photo, bday.date, bday.get_age()
        today_bdays.append(info)

    next_bdays = []
    for bday in next_birthdays:
        info = bday.id, bday.title, bday.content, bday.photo, bday.date, bday.get_age()
        next_bdays.append(info)

    return today_bdays, next_bdays


async def show_soon_birthdays(message: Message, bot: Bot):

    id_chat = message.from_user.id

    today_birthdays, next_birthdays = await set_bdays(id_chat, 'soon')

    if today_birthdays:
        await message.answer('Сьогодні святкуємо:')
        for birthday in today_birthdays:
            await send_birthday_date(bot, id_chat, birthday)
    if next_birthdays:
        await message.answer('Незабаром святкуємо:')
        for birthday in next_birthdays:
            await send_birthday_date(bot, id_chat, birthday)
