import pytz
from aiogram import Bot
from asgiref.sync import sync_to_async

from happy_bday.settings import TIME_ZONE
from happy_bot.core.handlers.check_user import check_user
from happy_bot.core.handlers.reminders import send_reminder_date, get_user_for_user_id, Info, send_birthday_date, BDinfo
from happy_bot.core.keyboards.inline import month_names
from happy_site.models import Reminder, BDays


async def show_bdays_for_name(id_chat: int, name: str, bot: Bot):
    birthdays = await set_bdays_name(id_chat, name)
    if not birthdays:
        await bot.send_message(id_chat, '\U0001F916\n\nНемає Днів народження для обраного іменинника...')
    else:
        await bot.send_message(id_chat, f"\U0001F916\n\nДень народження для <b>{name.upper()}</b>:")
        for birthday in birthdays:
            await send_birthday_date(bot, id_chat, birthday)


async def set_bdays_name(chat_id: int, name: str) -> list[BDinfo]:
    user_id, user_name = await check_user(chat_id)
    user = await get_user_for_user_id(user_id)
    birthdays = await get_bdays_for_name(user, name)

    information = []
    for bday in birthdays:
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
def get_bdays_for_name(user, name):
    bdays = BDays.objects.filter(user_id=user, title__contains=name)
    birthdays = []
    for bday in bdays:
        info = bday.id, bday.title, bday.content, bday.photo, bday.date, bday.get_age()
        birthdays.append(info)

    return birthdays

