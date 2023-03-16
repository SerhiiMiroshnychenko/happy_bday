"""БАЗОВІ ОБРОБНИКИ НАГАДУВАНЬ ТА ДНІВ НАРОДЖЕНЬ"""

# Базові імпорти
import pytz
from datetime import datetime

# Перетворення sync та async
from asgiref.sync import sync_to_async

# Імпорти Aiogram
from aiogram import Bot
from aiogram.types import Message

# Імпорти Django
from django.db.models import QuerySet
from django.contrib.auth.models import User

# Імпорт з пакета налаштувань
from happy_bday.settings import TIME_ZONE
from happy_bot.bot_exceptions import BotException

# Імпорти з app-ки сайту
from happy_site.models import Reminder, BDays

# Внутрішні імпорти
from happy_bot.core.handlers.send_media import get_picture
from happy_bot.core.utils.named_tuple_classes import RInfo, BDinfo
from happy_bot.core.handlers.send_bday_date import send_birthday_date
from happy_bot.core.handlers.birthdays_name_handlers import make_bdays_list
from happy_bot.core.handlers.data_inline_handlers import make_reminders_information
from happy_bot.core.handlers.check_user import check_user, get_user_for_user_id, remind_about_auth

"""REMINDERS"""


# Запит в базу даних за нагадуваннями для користувача
@sync_to_async
def get_reminders(id_user: int) -> list[tuple]:
    """
    The get_reminders function takes in an id_user and returns a list of tuples containing the following information:
        - reminder id
        - birthday title (name)
        - birthday date (date)
        - age of person on next birthday (int)

    :param id_user: int: Get the reminders for a specific user
    :return: A list of tuples
    """
    rems = Reminder.objects.filter(user_id=id_user)
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
async def send_reminder_date(bot: Bot, chat_id: int, reminder: RInfo) -> None:
    """
    The send_reminder_date function sends a reminder to the user about the date of birth.


    :param bot: Bot: Pass the bot object to the function
    :param chat_id: int: Send the message to a specific chat
    :param reminder: Info: Pass the reminder object to the function
    :return: None; Send the date of the reminder
    """
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
async def set_reminders(chat_id: int = None) -> list[RInfo] or None:
    """
    The set_reminders function is used to get all reminders for a user.
        Args:
            chat_id (int): The Telegram chat id of the user.

    :param chat_id: int: Identify the user
    :return: A list of reminders' information
    """
    user_id, user_name = await check_user(chat_id)
    reminders = []
    if not user_id:
        return None
    try:
        user = await get_user_for_user_id(user_id)
        reminders = await get_reminders(user)
    except BotException as error:
        print(error.__class__, error)
    return await make_reminders_information(reminders)


async def show_reminders_for_message(message: Message, bot: Bot) -> None:
    """
    The show_reminders_for_message function is a coroutine that takes in a message and bot object.
    It then calls the show_reminders_for_id function with the chat id of the user who sent the message.

    :param message: Message: Get the user id from the message
    :param bot: Bot: Send messages to the user
    :return: Nothing, so it is of type none
    """
    chat_id = message.from_user.id
    await show_reminders_for_id(chat_id, bot)


async def show_reminders_for_id(id_chat: int, bot: Bot) -> None:
    """
    The show_reminders_for_id function is used to display all reminders for a given chat.
        It takes in the id of the chat and a bot object, then it uses the set_reminders function
        to get all reminders for that chat. If there are any, it iterates through them and sends each one using
        send_reminder_date.

    :param id_chat: int: Get the reminders for a specific chat
    :param bot: Bot: Send the reminder to the user
    :return: None; Set a list of reminders
    """
    if reminders := await set_reminders(id_chat):
        for reminder in reminders:
            await send_reminder_date(bot, id_chat, reminder)
    else:
        return None


"""BIRTHDAYS"""


async def show_birthdays_for_id(id_chat: int, bot: Bot) -> None:
    """
    The show_birthdays_for_id function is used to display all the birthdays in a chat.
        It takes two arguments: id_chat and bot. The id_chat argument is an integer that represents the ID of a chat,
        while the bot argument is an instance of Bot class from pyrogram library.

    :param id_chat: int: Specify the chat id for which we want to show the birthdays
    :param bot: Bot: Send messages to the chat
    :return: Nothing
    """
    birthdays = await set_bdays(id_chat)
    for birthday in birthdays:
        await send_birthday_date(bot, id_chat, birthday)


async def set_bdays(chat_id: int = None, version: str = None) -> list[BDinfo] or tuple[list[BDinfo], list[BDinfo]]:
    """
    The set_bdays function is used to get the birthdays of all users in a chat.
        It can be called with no arguments, or with one argument: version.
        If version is not specified, it will return a list of BDinfo objects for each user in the chat.
        If version == 'soon', it will return two lists: one containing BDinfo objects for users whose birthday
        has passed this year, and another containing BDinfo objects for users whose birthday has not yet passed
        this year.

    :param chat_id: int: Get the user_id of the user who sent the message
    :param version: str: Determine whether the user wants to see all birthdays or only those that are soon
    :return: A list of BDinfo objects or tuple[list[BDinfo], list[BDinfo]]

    """
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
def get_bdays(id_user: int) -> list[tuple]:
    """
    The get_bdays function takes in an id_user and returns a list of tuples containing the following information:
        - bday.id, bday.title, bday.content, bday.photo, bday.date


    :param id_user: int: Get the user id
    :return: A list of tuples
    """
    bdays = BDays.objects.filter(user_id=id_user)
    birthdays = []
    for bday in bdays:
        info = bday.id, bday.title, bday.content, bday.photo, bday.date, bday.get_age()
        birthdays.append(info)
    return birthdays


"""SOON BIRTHDAYS"""


# Отримуємо сьогоднішню дату
@sync_to_async
def get_soon_bdays(user: User) -> tuple[list, list]:
    """
    The get_soon_bdays function returns a tuple of two lists.
    The first list contains the birthdays that are today, and the second list contains
    the birthdays that are tomorrow. Each item in each list is a dictionary containing
    the birthday's title, date, and age.

    :param user: User: Get the user's birthday list
    :return: A tuple of two lists
    """
    today = datetime.now()

    # Знаходимо сьогоднішні дні народження
    today_birthdays = BDays.objects.filter(
        date__month=today.month,
        date__day=today.day,
        user=user
    ).order_by('date', 'title')

    # Знаходимо наступні дні народження
    birthdays = BDays.objects.filter(user=user).order_by('date__month', 'date__day', 'title')
    next_day_month = get_next_day_month(today, birthdays)
    next_birthdays = BDays.objects.filter(
        date__month=next_day_month[1],
        date__day=next_day_month[0],
        user=user
    ).order_by('date', 'title')
    today_bdays = get_bday_info_list(today_birthdays)
    next_bdays = get_bday_info_list(next_birthdays)

    return today_bdays, next_bdays


def get_bday_info_list(birthdays: QuerySet) -> list[tuple]:
    """
    The get_bday_info_list function takes a QuerySet of birthdays and returns a list of tuples containing the
    following information about each birthday: id, title, content, photo (url), date (as string), age.


    :param birthdays: QuerySet: Pass in the list of birthdays from the database
    :return: A list of tuples
    """
    return [(bday.id, bday.title, bday.content, bday.photo, bday.date, bday.get_age()) for bday in birthdays]


def get_next_day_month(today: datetime, birthdays: QuerySet) -> tuple[int, int]:
    """
    The get_next_day_month function takes in a datetime object and a QuerySet of birthdays.
    It then iterates through the QuerySet, checking if any of the birthdays are in the current month.
    If they are, it checks to see if they're after today's date.
    If so, it returns that birthday's day and month as integers.

    :param today: datetime: Pass in the current date
    :param birthdays: QuerySet: Pass the queryset of birthdays to the function
    :return: The day and month of the next birthday
    """
    for birthday in birthdays:
        bday_month = birthday.date.month
        bday_day = birthday.date.day
        if (
                bday_month == today.month
                and bday_day > today.day
                or bday_month != today.month
                and bday_month > today.month
        ):
            return birthday.date.day, birthday.date.month


async def show_soon_birthdays(message: Message, bot: Bot) -> None:
    """
    The show_soon_birthdays function is used to show the user all of their upcoming birthdays.
        It takes in a message and bot object, and returns None.

    :param message: Message: Get the message that was sent by the user
    :param bot: Bot: Send messages to the user
    :return: None; Send a list of all upcoming birthdays
    """
    id_chat = message.from_user.id

    if (await check_user(message.from_user.id))[0]:
        today_birthdays, next_birthdays = await set_bdays(id_chat, 'soon')

        if today_birthdays:
            await message.answer('Сьогодні святкуємо:')
            for birthday in today_birthdays:
                await send_birthday_date(bot, id_chat, birthday)
        if next_birthdays:
            await message.answer('Незабаром святкуємо:')
            for birthday in next_birthdays:
                await send_birthday_date(bot, id_chat, birthday)
    else:
        await remind_about_auth(message.from_user.id)
