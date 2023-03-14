from aiogram import Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram.types import CallbackQuery

from happy_bot.bd_bot import bot
from happy_bot.core.handlers.birthdays_name_handlers import show_bdays_for_name
from happy_bot.core.keyboards.inline import get_rem_bd_keyboard, get_months_keyboard
from happy_bot.core.states.rem_name_state import RemNameState
from happy_bot.core.handlers.reminders_name_handlers import show_rems_for_name
from happy_bot.core.utils.callbackdata import Search


async def get_rem_bd(message: Message):
    await message.answer('\U0001F916\n\nОберіть подальшу дію:',
                         reply_markup=get_rem_bd_keyboard(message.from_user.id, message.text))


async def show_month_ver(call: CallbackQuery, bot: Bot, callback_data: Search):
    print('\n\n\n_____OK-1 from show_month_ver______\n\n\n')
    await call.message.answer('\U0001F916\n\nОберіть місяць:',
                               reply_markup=get_months_keyboard(
                                   callback_data.user_id,
                                   callback_data.search_object
                               ))
    print('\n\n\n_____OK-2 from show_month_ver______\n\n\n')


async def ask_name(call: CallbackQuery, callback_data: Search, state: FSMContext):
    await state.update_data(search_object=callback_data.search_object)
    await call.message.answer("\U0001F916\n\nВведіть ім'я чи прізвище іменинника:")
    await state.set_state(RemNameState.waiting_for_name)


async def process_name(message: Message, state: FSMContext):
    await message.answer("\U0001F916\n\nВеду пошук...")
    await state.update_data(name=message.text)
    print(f'\n\n____{message.text=}____\n\n')
    data = await state.get_data()
    name = data['name']
    f_object = data['search_object']
    print(f'{name=}')
    print(f'{type(name)=}')
    print(f'{f_object=}')

    if type(name) == str and f_object == 'Нагадування':
        print('\n\n____STR in process_name____\n\n')
        await show_rems_for_name(message.from_user.id, name, bot)
    elif type(name) == str and f_object == 'Д.Народження':
        await show_bdays_for_name(message.from_user.id, name, bot)
    else:
        print('\n\n____no STR in process_name____\n\n')
        await message.answer("\U0001F916\n\nІменинника не знайдено...")

    await state.clear()



