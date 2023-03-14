from aiogram import Bot
from aiogram.types import CallbackQuery

from .reminders import show_reminders, show_reminders_for_id, set_reminders, send_reminder_date, show_birthdays_for_id
from .reminders_inline_handlers import show_rems_for_month, show_rb_for_month
from ..utils.callbackdata import MacInfo, Search
from ...bd_bot import bot


async def select_macbook(call: CallbackQuery, bot: Bot, callback_data: MacInfo):
    model = callback_data.model
    size = callback_data.size
    chip = callback_data.chip
    year = callback_data.year
    answer_ = f'Tи обрав Aplle Macbook {model} з діагоналлю {size} дюймів, ' \
              f'на чіпі {chip} {year} року.'
    await call.message.answer(answer_)
    await call.answer()


async def select_answer(call: CallbackQuery, bot: Bot):

    answer_ = call.data
    await call.message.answer(answer_)
    await call.answer()


async def select_rem_bd(call: CallbackQuery, bot: Bot, callback_data: Search):
    chat_id = callback_data.user_id
    find_object = callback_data.search_object
    await call.message.answer(f'\U0001F916\n\nВСІ {find_object.upper()}:')
    match find_object:
        case 'Нагадування':
            await show_reminders_for_id(chat_id, bot)
        case 'Д.Народження':
            await show_birthdays_for_id(chat_id, bot)


async def show_rem_bd(call: CallbackQuery, bot: Bot, callback_data: Search):
    chat_id = callback_data.user_id
    find_object = callback_data.search_object

    reminders = await set_reminders(chat_id)
    for reminder in reminders:
        await send_reminder_date(bot, chat_id, reminder)


async def select_months(callback_query: CallbackQuery):
    user_id = int(callback_query.data.split('_')[1])
    month_number = int(callback_query.data.split('_')[2])
    f_object = callback_query.data.split('_')[-1]

    await show_rb_for_month(user_id, month_number, f_object, bot)


