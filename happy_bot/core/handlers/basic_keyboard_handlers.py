from aiogram import Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram.types import CallbackQuery

from happy_bot.bd_bot import bot
from happy_bot.core.keyboards.inline import get_reminders_keyboard, get_months_keyboard
from happy_bot.core.states.rem_name_state import RemNameState
from happy_bot.core.handlers.reminders_name_handlers import show_rems_for_name


async def get_rem(message: Message):
    await message.answer('Оберіть подальшу дію:',
                         reply_markup=get_reminders_keyboard(message.from_user.id))


async def show_month_ver(query: CallbackQuery):
    print('\n\n\n_____OK-1 from show_month_ver______\n\n\n')
    await query.message.answer('Оберіть місяць:',
                         reply_markup=get_months_keyboard(query.from_user.id))
    print('\n\n\n_____OK-2 from show_month_ver______\n\n\n')


async def ask_name(query: CallbackQuery, state: FSMContext):
    await query.message.answer("\U0001F916\n\nВведіть ім'я чи прізвище іменинника:")
    await state.set_state(RemNameState.waiting_for_name)


async def process_name(message: Message, state: FSMContext):
    await message.answer("Веду пошук:")
    await state.update_data(name=message.text)
    print(f'\n\n____{message.text=}____\n\n')
    data = await state.get_data()
    name = data['name']
    print(f'{name=}')
    print(f'{type(name)=}')

    if type(name) == str:
        print('\n\n____STR in process_name____\n\n')
        await show_rems_for_name(message.from_user.id, name, bot)
    else:
        print('\n\n____no STR in process_name____\n\n')
        await message.answer("Ім'я не знайдено")

    await state.clear()




