# Імпорти Aiogram
from aiogram.types import Message

# Внутрішні імпорти
from happy_bot.bd_bot import bot
from happy_bot.core.handlers.send_media import get_picture


async def send_message_glory(chat_id: int) -> None:
    """
    The send_message_glory function sends a message to the user with chat_id.
        Args:
            chat_id (int): The id of the Telegram Chat where we want to send our message.

    :param chat_id: int: Specify the chat id of the message recipient
    :return: None
    """
    await bot.send_message(chat_id, 'Слава Нації!')


async def send_message_chat_gpt(message: Message) -> None:
    """
    The send_message_chat_gpt function is a coroutine that sends a message to the user.
        Args:
            message (Message): The Telegram Message object containing information about the chat and sender.

    :param message: Message: Get the message that was sent by the user
    :return: None
    """
    await get_picture(message.from_user.id, bot, 'Я, звісно, не ChatGPT, але спробую допомогти)', 'chat')
