import pytz
from aiogram import Bot
from asgiref.sync import sync_to_async

from happy_bday.settings import TIME_ZONE
from happy_bot.core.handlers.check_user import check_user
from happy_bot.core.handlers.reminders import send_reminder_date, get_user_for_user_id, Info, BDinfo, send_birthday_date
from happy_bot.core.keyboards.inline import month_names
from happy_site.models import Reminder, BDays


async def show_rems_for_month(id_chat: int, month_number: int, bot: Bot):
    reminders = await set_rems(id_chat, month_number)
    if not reminders:
        await bot.send_message(id_chat, '\U0001F916\n\nНемає нагадувань для обраного місяця...')
    else:
        await bot.send_message(id_chat, f"\U0001F916\n\nНагадування за <b>{month_names[month_number].upper()}</b>:")
        for num, reminder in enumerate(reminders):
            await send_rem_date(bot, id_chat, num, reminder)


async def set_rems(chat_id: int, month_number: int) -> list[Info]:
    user_id, user_name = await check_user(chat_id)
    user = await get_user_for_user_id(user_id)
    reminders = await get_rems_for_month(user, month_number)

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


@sync_to_async
def get_rems_for_month(user, month_number):
    rems = Reminder.objects.filter(user_id=user, date_time__month=month_number)

    reminders = []
    for rem in rems:
        birthday = BDays.objects.get(id=rem.bday_id)
        info = rem.id, birthday.title, birthday.date, birthday.get_age(), rem.text, rem.date_time
        reminders.append(info)

    return reminders


async def send_rem_date(bot: Bot, chat_id: int, num: int, reminder: Info):
    message = f'Нагадування №{num + 1}\n' \
              f'<b>{reminder.title.upper()}</b>\n' \
              f'<b>{reminder.birth_date.strftime("%d.%m.%Y")}</b>\n' \
              f'Виповнюється:  <b>{reminder.age}</b> років\n' \
              f' Дата нагадування:  ' \
              f'{reminder.rem_time.astimezone(tz=pytz.timezone(TIME_ZONE)).strftime("%d.%m о %H:%M")}\n'
    await bot.send_message(chat_id, message)


async def show_rb_for_month(id_chat: int, month_number: int, s_object: str, bot: Bot):
    await bot.send_message(id_chat, f"\U0001F916\n\n{s_object} за <b>{month_names[month_number].upper()}</b>:")
    objects = None
    match s_object:
        case 'Нагадування':
            objects = await set_rems(id_chat, month_number)
            for num, rem in enumerate(objects):
                await send_rem_date(bot, id_chat, num, rem)
        case 'Д.Народження':
            objects = await set_bdays(id_chat, month_number)
            for bday in objects:
                await send_birthday_date(bot, id_chat, bday)
    if not objects:
        await bot.send_message(id_chat,
                               f'\U0001F916\n\nНемає жодного {s_object.upper()} для обраного місяця...')


async def set_bdays(chat_id: int, month_number: int) -> list[BDinfo]:
    user_id, user_name = await check_user(chat_id)
    user = await get_user_for_user_id(user_id)
    bdays = await get_bdays_for_month(user, month_number)

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
def get_bdays_for_month(user, month_number):
    bdays = BDays.objects.filter(user_id=user, date__month=month_number)

    birthdays = []
    for bday in bdays:
        info = bday.id, bday.title, bday.content, bday.photo,  bday.date, bday.get_age()
        birthdays.append(info)

    return birthdays
