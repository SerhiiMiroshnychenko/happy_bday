from aiogram import Bot
from aiogram.types import Message
from aiogram.types import CallbackQuery

from happy_bot.core.keyboards.inline import get_reminders_keyboard, get_months_keyboard


async def get_rem(message: Message):
    await message.answer('Оберіть подальшу дію:',
                         reply_markup=get_reminders_keyboard(message.from_user.id))


async def show_month_ver(query: CallbackQuery):
    print('\n\n\n_____OK-1 from show_month_ver______\n\n\n')
    await query.message.answer('Оберіть місяць:',
                         reply_markup=get_months_keyboard(query.from_user.id))
    print('\n\n\n_____OK-2 from show_month_ver______\n\n\n')

