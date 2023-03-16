"""ОБРОБНИКИ ДЛЯ ПОШУКУ ТА СОРТУВАННЯ НАГАДУВАНЬ ЗА ІМЕНИННИКОМ"""

# Імпорти Aiogram
from aiogram import Bot

# Внутрішні імпорти
from happy_bot.core.handlers.check_user import check_user
from happy_bot.core.handlers.data_inline_handlers \
    import make_reminders_information, get_reminders_for_param, send_reminders_data
from happy_bot.core.handlers.reminders_and_birthdays import get_user_for_user_id, Info


async def show_reminders_for_name(id_chat: int, name: str, bot: Bot) -> None:
    """
    The show_reminders_for_name function is used to show all reminders for a specific name.
        It takes the id_chat and name as arguments, and returns None.

    :param id_chat: int: Get the reminders for a specific chat
    :param name: str: Get the reminders for a specific name
    :param bot: Bot: Send a message to the user
    :return: None; Send a list of reminders for a given name
    """
    reminders = await set_reminders_by_name(id_chat, name)
    if not reminders:
        await bot.send_message(id_chat, '\U0001F916\n\nНемає нагадувань для обраного іменинника...')
    else:
        await bot.send_message(id_chat, f"\U0001F916\n\nНагадування для <b>{name.upper()}</b>:")
        for num, reminder in enumerate(reminders):
            await send_reminders_data(bot, id_chat, num, reminder)


async def set_reminders_by_name(chat_id: int, name: str) -> list[Info]:
    """
    The set_reminders_by_name function is used to get a list of reminders for a user by name.
        Args:
            chat_id (int): The Telegram ID of the user who sent the message.
            name (str): The name of the reminder(s) that are being searched for.

    :param chat_id: int: Identify the user
    :param name: str: Get the reminders for a specific user
    :return: A list of Info objects
    """
    user_id, user_name = await check_user(chat_id)
    user = await get_user_for_user_id(user_id)
    reminders = await get_reminders_for_param(user, name)
    return await make_reminders_information(reminders)
