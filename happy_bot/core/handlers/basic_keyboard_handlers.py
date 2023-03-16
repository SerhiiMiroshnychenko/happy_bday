"""ОБРОБНИКИ КНОПОК ОСНОВНОЇ КЛАВІАТУРИ ТА ДЕЯКИХ INLINE КНОПОК"""

# Імпорти Aiogram
from aiogram.types import Message
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext

# Внутрішні імпорти
from happy_bot.bd_bot import bot
from happy_bot.core.handlers.check_user import check_user, remind_about_auth
from happy_bot.core.utils.callbackdata import Search
from happy_bot.core.states.rem_name_state import RemNameState
from happy_bot.core.handlers.reminders_name_handlers import show_reminders_for_name
from happy_bot.core.handlers.birthdays_name_handlers import show_bdays_for_name
from happy_bot.core.keyboards.inline import get_reminders_birthdays_keyboard, get_months_keyboard


async def get_reminders_birthdays(message: Message) -> None:

    """
    The get_reminders_birthdays function is a coroutine that sends a message to the user from
      a keyboard that includes reminders/birthdays actions. The user can then choose
      what they want to do next.


    :param message: Message: Get the user id and message text
    :return: The keyboard for the user to choose further action
    """
    if (await check_user(message.from_user.id))[0]:
        await message.answer('\U0001F916\n\nОберіть подальшу дію:',
                             reply_markup=get_reminders_birthdays_keyboard(
                                 message.from_user.id, message.text))
    else:
        await remind_about_auth(message.from_user.id)


async def show_month_ver(call: CallbackQuery, callback_data: Search) -> None:
    """
    The show_month_ver function is a callback handler for the /search command.
    It shows the user a list of months to choose from, and then calls show_day_ver
    to display reminders or birthdays in that month.

    :param call: CallbackQuery: Get the message that was sent by the user
    :param callback_data: Search: Get the user_id and search_object
    :return: None; Send a keyboard with months
    """
    if (await check_user(call.from_user.id))[0]:
        await call.message.answer('\U0001F916\n\nОберіть місяць:',
                                  reply_markup=get_months_keyboard(
                                      callback_data.user_id,
                                      callback_data.search_object
                                  ))
    else:
        await remind_about_auth(call.from_user.id)


async def ask_name(call: CallbackQuery, callback_data: Search, state: FSMContext) -> None:
    """
    The ask_name function is a callback handler for the search_by_name button.
    It updates the state data with the search object and asks for a name to be entered.


    :param call: CallbackQuery: Get the message object from the callback query
    :param callback_data: Search: Pass the data from the previous state to this one
    :param state: FSMContext: Store the state of the conversation
    :return: None; Save search_object in state's data.
    """
    if (await check_user(call.from_user.id))[0]:
        await state.update_data(search_object=callback_data.search_object)
        await call.message.answer("\U0001F916\n\nВведіть ім'я чи прізвище іменинника:")
        await state.set_state(RemNameState.waiting_for_name)
    else:
        await state.clear()
        await remind_about_auth(call.from_user.id)


async def process_name(message: Message, state: FSMContext) -> None:
    """
    The process_name function is a callback function that will be called when the user
        sends a message to the bot. It will process the person's name and return
        information about birthdays or reminders associated with this name.

    :param message: Message: Get the message that was sent by the user
    :param state: FSMContext: Store information about the conversation
    :return: The following:
    """
    await message.answer("\U0001F916\n\nВеду пошук...")
    await state.update_data(name=message.text)
    data = await state.get_data()
    name = data['name']
    f_object = data['search_object']

    if type(name) == str and f_object == 'Нагадування':
        await show_reminders_for_name(message.from_user.id, name, bot)
    elif type(name) == str and f_object == 'Д.Народження':
        await show_bdays_for_name(message.from_user.id, name, bot)
    else:
        await message.answer("\U0001F916\n\nІменинника не знайдено...")

    await state.clear()
