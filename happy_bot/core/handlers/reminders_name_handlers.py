import pytz
from aiogram import Bot
from asgiref.sync import sync_to_async

from happy_bday.settings import TIME_ZONE
from happy_bot.core.handlers.check_user import check_user
from happy_bot.core.handlers.reminders import send_reminder_date, get_user_for_user_id, Info
from happy_bot.core.keyboards.inline import month_names
from happy_site.models import Reminder, BDays


async def show_rems_for_name(id_chat: int, name: str, bot: Bot):
    reminders = await set_rems_name(id_chat, name)
    if not reminders:
        await bot.send_message(id_chat, '\U0001F916\n\nНемає нагадувань для обраного іменинника...')
    else:
        await bot.send_message(id_chat, f"\U0001F916\n\nНагадування для <b>{name.upper()}</b>:")
        for num, reminder in enumerate(reminders):
            await send_rem_date(bot, id_chat, num, reminder)


async def set_rems_name(chat_id: int, name: str) -> list[Info]:
    user_id, user_name = await check_user(chat_id)
    user = await get_user_for_user_id(user_id)
    reminders = await get_rems_for_name(user, name)

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
def get_rems_for_name(user, name):
    rems = Reminder.objects.filter(user_id=user, bday__title__contains=name)
    reminders = []
    for rem in rems:
        birthday = BDays.objects.get(id=rem.bday_id)
        info = rem.id, birthday.title, birthday.date, birthday.get_age(), rem.text, rem.date_time
        reminders.append(info)

    return reminders


async def send_rem_date(bot: Bot, chat_id: int, num: int, reminder: Info):
    message = f'Нагадування №{num+1}\n' \
              f'<b>{reminder.title.upper()}</b>\n' \
              f'<b>{reminder.birth_date.strftime("%d.%m.%Y")}</b>\n' \
              f'Виповнюється:  <b>{reminder.age}</b> років\n' \
              f' Дата нагадування:  ' \
              f'{reminder.rem_time.astimezone(tz=pytz.timezone(TIME_ZONE)).strftime("%d.%m о %H:%M")}\n'
    await bot.send_message(chat_id, message)