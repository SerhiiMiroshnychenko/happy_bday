from aiogram import Bot
from aiogram.types import Message

from happy_bot.bd_bot import bot
from happy_bot.core.handlers.send_media import get_picture


async def send_message_glory(bot: Bot, chat_id: int):
    await bot.send_message(chat_id, 'Слава Нації!')


async def send_message_chat_gpt(message: Message):
    await get_picture(message.from_user.id, bot, 'Я, звісно, не ChatGPT, але спробую допомогти)', 'chat')
