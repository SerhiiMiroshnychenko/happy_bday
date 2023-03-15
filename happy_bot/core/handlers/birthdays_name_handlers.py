"""ОБРОБНИКИ ПОШУКУ ТА СОРТУВАННЯ ДНІВ НАРОДЖЕНЬ ЗА ІМЕНИННИКОМ"""

# Перетворення sync та async
from asgiref.sync import sync_to_async

# Імпорти Aiogram
from aiogram import Bot

# Імпорти Django
from django.db.models import QuerySet
from django.contrib.auth.models import User

# Імпорти з app-ки сайту
from happy_site.models import BDays

# Внутрішні імпорти
from happy_bot.core.utils.named_tuple_classes import BDinfo
from happy_bot.core.handlers.send_bday_date import send_birthday_date
from happy_bot.core.handlers.check_user import check_user, get_user_for_user_id


async def show_bdays_for_name(id_chat: int, name: str, bot: Bot) -> None:
    """
    The show_bdays_for_name function is used to display all the birthdays for a given name.
        It takes in an id_chat, a name and a bot as parameters.
        The function first calls the set_bdays_name function which returns all the birthdays for that particular name.
        If there are no birthdays found, it sends back an appropriate message to the user via send_message().
        Otherwise, it sends back another message with information about how many birthday dates were found and
        then loops through each of them calling send_birthday().

    :param id_chat: int: Identify the chat where the message was sent
    :param name: str: Get the birthdays for a specific name
    :param bot: Bot: Send messages to the user
    :return: None
    """
    birthdays = await set_bdays_name(id_chat, name)
    if not birthdays:
        message_for_user = '\U0001F916\n\nНемає Днів народження для обраного іменинника...'
        await bot.send_message(id_chat, message_for_user)
    else:
        message_for_user = f"\U0001F916\n\nДень народження для <b>{name.upper()}</b>:"
        await bot.send_message(id_chat, message_for_user)
        for birthday in birthdays:
            await send_birthday_date(bot, id_chat, birthday)


async def set_bdays_name(chat_id: int, name: str) -> list[BDinfo]:
    """
    The set_bdays_name function is used to get all the birthdays for a specific name.
        It takes in a chat_id and name, then returns a list of BDinfo objects.

    :param chat_id: int: Get the user_id from the chat_id
    :param name: str: Find the birthday with that name
    :return: A list of BDinfo objects
    """
    user_id, user_name = await check_user(chat_id)
    user = await get_user_for_user_id(user_id)
    print(f'{type(user)}')
    birthdays = await get_bdays_for_name(user, name)

    return await make_bdays_list(birthdays)


async def make_bdays_list(bdays: list[tuple]) -> list[BDinfo]:
    """
    The make_bdays_list function takes a list of tuples and returns a list of BDinfo objects.
        The function is used to convert the results from the database into an object that can be easily manipulated.

    :param bdays: list[tuple]: Pass in a list of tuples
    :return: A list of BDinfo objects
    """
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

    return information


@sync_to_async
def get_bdays_for_name(user: User, name: str) -> list[tuple]:
    """
    The get_bdays_for_name function takes in a user and a name, and returns all birthdays that contain the given name.


    :param user: User: Filter the bdays table for a specific user
    :param name: str: Filter the bdays by name
    :return: A list of tuples
    """
    bdays = BDays.objects.filter(user_id=user, title__contains=name)
    return make_bdays_list_for_filtering(bdays)


def make_bdays_list_for_filtering(bdays: QuerySet) -> list[tuple]:
    """
    The make_bdays_list_for_filtering function takes a QuerySet of birthdays and returns a list of tuples.
    Each tuple contains the id, title, content, photo url (if any), date and age for each birthday in the QuerySet.

    :param bdays: QuerySet: Pass in a queryset of birthdays
    :return: A list of tuples
    """
    birthdays = []
    for bday in bdays:
        info = bday.id, bday.title, bday.content, bday.photo, bday.date, bday.get_age()
        birthdays.append(info)
    return birthdays
