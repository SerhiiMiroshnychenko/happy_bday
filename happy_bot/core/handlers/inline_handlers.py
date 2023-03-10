from aiogram import Bot
from aiogram.types import Message

from happy_bot.core.keyboards.inline import get_macbook_keyboard


async def get_macbook(message: Message):
    await message.answer(f'Привіт, {message.from_user.first_name}. Вибір macbook-ів: ',
                         reply_markup=get_macbook_keyboard())

