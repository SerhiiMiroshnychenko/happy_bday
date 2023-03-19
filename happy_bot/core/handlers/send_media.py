# Імпорти Aiogram
from aiogram import Bot
from aiogram.types import FSInputFile

# Внутрішні імпорти
from happy_bot.bot_exceptions import BotException


async def get_birthday_photo(chat_id: int, bot: Bot, text: str, photo_path: str) -> None:
    """
    The get_birthday_photo function is used to send a birthday photo with the text
        that was passed as an argument. The function takes in 4 arguments: chat_id, bot,
        text and photo_path. The first two are required by the telethon library for sending
        messages and photos to users on Telegram. The third argument is a string containing
        the message that will be sent along with the birthday photo while the fourth one is
        a string containing path of where our birthday photos are stored.
    :param chat_id: int: Send the message to a specific chat
    :param bot: Bot: Send the photo to the user
    :param text: str: Send a message to the user
    :param photo_path: str: Specify the path to the photo
    :return: None
    """
    bday_path = fr'/code/media/{photo_path}'
    try:
        birthday_photo = FSInputFile(path=bday_path,
                                     filename='BDayPerson.png')
        await bot.send_photo(chat_id, photo=birthday_photo, caption=text)
    except BotException as error:
        print(error)
        await bot.send_message(chat_id, text)


async def get_picture(chat_id: int, bot: Bot, text: str = None, name: str = None) -> None:

    """
    The get_picture function sends a picture to the user.
        Args:
            chat_id (int): The id of the chat where we want to send the message.
            bot (Bot): The bot that will be sending messages and pictures.
            text (str, optional): A string containing a caption for our picture.
            Defaults to None if not specified by user.
    :param chat_id: int: Send the picture to a specific chat
    :param bot: Bot: Send the photo to the user
    :param text: str: Send a message to the user with the picture
    :param name: str: Get the name of the person whose birthday it is,
    :return: None
    """
    try:
        reminder_picture = FSInputFile(path=fr'/code/happy_bot/static/happy_bot/images/{name}.png',
                                       filename=f'ItIs{name.title()}.png')
        await bot.send_photo(chat_id, photo=reminder_picture, caption=text)
    except BotException as error:
        print(error)
        await bot.send_message(chat_id, text)
