"""ОБРОБНИКИ INLINE КНОПОК ДЛЯ НАГАДУВАНЬ ТА ДНІВ НАРОДЖЕНЬ"""

# Базові імпорти
import pytz

# Перетворення sync та async
from asgiref.sync import sync_to_async

# Імпорти Aiogram
from aiogram import Bot

# Імпорти Django
from django.contrib.auth.models import User

# Імпорт з пакета налаштувань
from happy_bday.settings import TIME_ZONE

# Імпорти з app-ки сайту
from happy_site.models import Reminder, BDays

# Внутрішні імпорти
from happy_bot.core.keyboards.inline import month_names
from happy_bot.core.utils.named_tuple_classes import Info, BDinfo
from happy_bot.core.handlers.send_bday_date import send_birthday_date
from happy_bot.core.handlers.check_user import check_user, get_user_for_user_id
from happy_bot.core.handlers.birthdays_name_handlers import make_bdays_list, make_bdays_list_for_filtering


async def set_reminders(chat_id: int, month_number: int) -> list[Info]:
    """
    The set_reminders function is used to get all reminders for a given month.
        It takes in the chat_id of the user and the month number parameters,
        and returns a list of Info objects containing information about each reminder.

    :param chat_id: int: Identify the user
    :param month_number: int: Get the reminders for a specific month
    :return: A list of info objects
    """
    user_id, user_name = await check_user(chat_id)
    user = await get_user_for_user_id(user_id)
    reminders = await get_reminders_for_param(user, month_number)

    return await make_reminders_information(reminders)


async def make_reminders_information(reminders: list[tuple]) -> list[Info]:
    """
    The make_reminders_information function takes a list of tuples and returns a list of Info objects.
    The function is used to convert the reminders from the database into Info objects that can be sent to the client.

    :param reminders: list[tuple]: Pass the list of tuples that is returned from the get_reminders function
    :return: A list of info objects
    """
    return [Info(id=reminder[0],
                 title=reminder[1],
                 birth_date=reminder[2],
                 age=reminder[3],
                 text=reminder[4],
                 rem_time=reminder[5])
            for reminder in reminders]


@sync_to_async
def get_reminders_for_param(user: User, param: int or str) -> list[tuple]:
    """
    The get_reminders_for_param function takes in a user and a parameter.
    The parameter can be an integer or string. If the param is an int, it will return all reminders for that month.
    If the param is a string, it will return all reminders with birthdays containing that string in their title (name).
    If no param is given, it returns all the users' reminders.

    :param user: User: Get the reminders for a specific user
    :param param: int or str: Filter the reminders by month or name
    :return: A list of tuples with the following structure:
    """
    if type(param) == int:
        rems = Reminder.objects.filter(user_id=user, date_time__month=param)
    elif type(param) == str:
        rems = Reminder.objects.filter(user_id=user, bday__title__contains=param)
    else:
        rems = Reminder.objects.filter(user_id=user)
    reminders = []
    for rem in rems:
        birthday = BDays.objects.get(id=rem.bday_id)
        info = rem.id, birthday.title, birthday.date, birthday.get_age(), rem.text, rem.date_time
        reminders.append(info)

    return reminders


async def send_reminders_data(bot: Bot, chat_id: int, num: int, reminder: Info) -> None:
    """
    The send_reminders_data function sends a message to the user with information about the reminder.
        Args:
            bot (Bot): The Bot object that is used for sending messages.
            chat_id (int): The id of the chat where we want to send our message.
            num (int): Number of reminders in list, which will be sent next time when function called again.
                       It's needed for correct numbering of reminders in output message, and also it helps us
                       to know what reminder should be sent next time when this function is called again.

    :param bot: Bot: Send messages to the user
    :param chat_id: int: Send a message to the user who sent the command
    :param num: int: Display the number of reminders in the list
    :param reminder: Info: Pass the reminder object to the function
    :return: None; Send a message with a reminder
    """
    message = f'Нагадування №{num + 1}\n' \
              f'<b>{reminder.title.upper()}</b>\n' \
              f'<b>{reminder.birth_date.strftime("%d.%m.%Y")}</b>\n' \
              f'Виповнюється:  <b>{reminder.age}</b> років\n' \
              f' Дата нагадування:  ' \
              f'{reminder.rem_time.astimezone(tz=pytz.timezone(TIME_ZONE)).strftime("%d.%m о %H:%M")}\n'
    await bot.send_message(chat_id, message)


async def show_data_for_month(id_chat: int, month_number: int, s_object: str, bot: Bot) -> None:
    """
    The show_data_for_month function is used to display the data for a specific month.
        It takes in three arguments: id_chat, month_number and s_object. The first argument is an integer representing
        the chat ID of the user who sent a message to our bot. The second argument is an integer representing
        a number of some month. And finally, s_object represents either 'Нагадування'
        or 'День народження'.

    :param id_chat: int: Send the message to a specific chat
    :param month_number: int: Get the month number from the user
    :param s_object: str: Determine which type of data to show
    :param bot: Bot: Send messages to the user
    :return: None; Send a list of reminders or birthdays for the selected month
    """
    await bot.send_message(id_chat, f"\U0001F916\n\n{s_object} за <b>{month_names[month_number].upper()}</b>:")
    objects = None
    match s_object:
        case 'Нагадування':
            if objects := await set_reminders(id_chat, month_number):
                for num, rem in enumerate(objects):
                    await send_reminders_data(bot, id_chat, num, rem)
        case 'Д.Народження':
            if objects := await set_bdays(id_chat, month_number):
                for bday in objects:
                    await send_birthday_date(bot, id_chat, bday)
    if not objects:
        await bot.send_message(id_chat,
                               f'\U0001F916\n\nНемає жодного {s_object.upper()} для обраного місяця...')


async def set_bdays(chat_id: int, month_number: int) -> list[BDinfo]:
    """
    The set_bdays function is used to set the bdays list for a given month.
        It takes in a chat_id and month number, and returns a list of BDinfo objects.
        The function first checks if the user exists, then gets all birthdays for that user's friends
        who have birthdays in that month.

    :param chat_id: int: Identify the user
    :param month_number: int: Specify which month to get the birthdays for
    :return: A list of BDinfo objects
    """
    user_id, user_name = await check_user(chat_id)
    user = await get_user_for_user_id(user_id)
    bdays = await get_bdays_for_month(user, month_number)
    return await make_bdays_list(bdays)


@sync_to_async
def get_bdays_for_month(id_user: int, month_number: int) -> list[tuple]:
    """
    The get_bdays_for_month function takes in an id_user and a month_number,
    and returns a list of tuples containing the name and date of birthdays for that user.

    :param id_user: int: Filter the bdays objects by user_id
    :param month_number: int: Filter the bdays objects by month
    :return: A list of tuples,
    """
    bdays = BDays.objects.filter(user_id=id_user, date__month=month_number)
    return make_bdays_list_for_filtering(bdays)
