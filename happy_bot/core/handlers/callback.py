"""ОБРОБНИКИ CALLBACK QUERY"""

# Імпорти Aiogram
from aiogram import Bot
from aiogram.types import CallbackQuery

# Внутрішні імпорти
from happy_bot.bd_bot import bot
from happy_bot.core.handlers.check_user import check_user, remind_about_auth
from happy_bot.core.utils.callbackdata import Search
from happy_bot.core.handlers.reminders_inline_handlers import show_date_for_month
from happy_bot.core.handlers.reminders_and_birthdays\
    import show_reminders_for_id, set_reminders, send_reminder_date, show_birthdays_for_id


async def select_answer(call: CallbackQuery) -> None:
    """
    The select_answer function is a callback function that takes
     the user's answer to a question and sends it back to them.
     It also answers the CallbackQuery object, which removes the
     inline keyboard from view.

    :param call: CallbackQuery: Get the data from the callback query
    :return: None; Send the answer of the user
    """
    answer_ = call.data
    await call.message.answer(answer_)
    await call.answer()


async def select_reminder_birthday(call: CallbackQuery, callback_data: Search) -> None:
    """
    The select_reminder_birthday function is a callback handler for the select_reminder_birthday button.
    It shows all reminders or birthdays for a user.

    :param call: CallbackQuery: Get the message object that was sent by the user
    :param callback_data: Search: Get the user_id and search_object from the callback data
    :return: The user's reminders or birthdays
    """
    if (await check_user(call.from_user.id))[0]:
        chat_id = callback_data.user_id
        find_object = callback_data.search_object
        await call.message.answer(f'\U0001F916\n\nВСІ {find_object.upper()}:')
        match find_object:
            case 'Нагадування':
                await show_reminders_for_id(chat_id, bot)
            case 'Д.Народження':
                await show_birthdays_for_id(chat_id, bot)
    else:
        await remind_about_auth(call.from_user.id)


async def show_reminders_birthday(bot_: Bot, callback_data: Search) -> None:
    """
    The show_reminders_birthday function is called when the user clicks on the 'Birthday' button in
    the reminders' menu. It sends a message to the user with all of their birthday reminders.

    :param bot_: Bot: Send a message to the user
    :param callback_data: Search: Get the user_id from the callback data
    :return: Nothing
    """
    chat_id = callback_data.user_id

    reminders = await set_reminders(chat_id)
    for reminder in reminders:
        await send_reminder_date(bot_, chat_id, reminder)


async def select_months(callback_query: CallbackQuery) -> None:
    """
    The select_months function is called when a user clicks on one of the months.
    It then calls show_date_for_month to display.

    :param callback_query: CallbackQuery: Get the data from the callback query
    :return: A list of dates for a specific month
    """
    if (await check_user(callback_query.from_user.id))[0]:
        user_id = int(callback_query.data.split('_')[1])
        month_number = int(callback_query.data.split('_')[2])
        f_object = callback_query.data.split('_')[-1]

        await show_date_for_month(user_id, month_number, f_object, bot)
    else:
        await remind_about_auth(callback_query.from_user.id)
