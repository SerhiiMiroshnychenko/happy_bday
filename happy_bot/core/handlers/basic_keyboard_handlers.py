from aiogram import Bot
from aiogram.types import Message

from happy_bot.core.keyboards.inline import get_reminders_keyboard


async def get_rem(message: Message):
    await message.answer('Оберіть подальшу дію:',
                         reply_markup=get_reminders_keyboard(message.from_user.id))
