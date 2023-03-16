# Імпорти Aiogram
from aiogram import Bot

# Внутрішні імпорти
from happy_bot.core.utils.named_tuple_classes import BDinfo
from happy_bot.core.handlers.send_media import get_birthday_photo


async def send_birthday_date(bot: Bot, chat_id: int, birthday: BDinfo) -> None:
    """
    The send_birthday_date function sends a message to the user with birthday information.
        Args:
            bot (Bot): The Bot object that is used to send messages.
            chat_id (int): The id of the chat where the message will be sent.
            birthday (BDinfo): A BDinfo object containing all relevant information about a person's birthday.

    :param bot: Bot: Pass the bot object to the function
    :param chat_id: int: Send the message to a specific chat
    :param birthday: BDinfo: Pass the birthday object to the function
    :return: None; Send a message with the birthday date
    """
    if birthday:
        message = f'<b>{birthday.title.upper()}</b>\n' \
                  f'{birthday.content}\n' \
                  f'<b>{birthday.birth_date.strftime("%d.%m.%Y")}</b>\n' \
                  f'Виповнюється:  <b>{birthday.age}</b> років\n\n' \

        if birthday.photo_path:
            await get_birthday_photo(chat_id, bot, message, birthday.photo_path)
        else:
            await bot.send_message(chat_id, message)
