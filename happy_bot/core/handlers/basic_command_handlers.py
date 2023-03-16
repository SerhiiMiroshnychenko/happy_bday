"""ОБРОБНИКИ ДЛЯ ОСНОВНИХ КОМАНД"""

# Базові імпорти
from datetime import datetime, timedelta

# Перетворення sync та async
from asgiref.sync import sync_to_async

# Імпорти Aiogram
from aiogram.types import Message

# Планувальник
from apscheduler.schedulers.asyncio import AsyncIOScheduler

# Внутрішні імпорти
from happy_bot.bd_bot import bot
from happy_bot.bot_exceptions import BotException
from happy_bot.models import Profile
from happy_bot.core.handlers.check_user import check_user, remind_about_auth
from happy_bot.core.handlers.send_media import get_picture
from happy_bot.core.keyboards.reply import get_reply_keyboard
from happy_bot.core.messages.bese_command_messages import help_message
from happy_bot.core.handlers.schedul_task import send_message_chat_gpt
from happy_bot.core.bot_scheduler.update_reminders import update_reminders_for_id
from happy_site.signals import sync_show_job

"""START"""


async def get_start(message: Message, apscheduler: AsyncIOScheduler) -> None:
    """
    The get_start function is responsible for handling the /start command.
    It sends a greeting message to the user and displays a list of available commands.

    :param message: Message: Get the user's id
    :param apscheduler: AsyncIOScheduler: Add a job to the scheduler
    :return: None; Send a message for the user
    """

    user_id, user_name = await check_user(message.from_user.id)
    start_message_for_auth = f'Вітаю, <b>{user_name} ({message.from_user.full_name})</b>,' \
                             f' чим можу допомогти?'
    start_message_for_not_auth = f'Вітаю, <b>{message.from_user.full_name}</b>, ' \
                                 f'я бот сайту <b>HAPPY B-DAYS</b>.\n' \
                                 f'Для ознайомлення з моїми можливостями оберіть команду "<b>/help</b>".'
    message_for_user = start_message_for_auth if user_id else start_message_for_not_auth

    await get_picture(message.from_user.id, bot, message_for_user, 'start')

    if user_id:
        await message.answer('Оберіть подальшу дію.', reply_markup=get_reply_keyboard())

        apscheduler.add_job(update_reminders_for_id, trigger='interval',
                            seconds=30,
                            kwargs={'bot': bot, 'chat_id': message.from_user.id})
    else:
        await remind_about_auth(message.from_user.id)


"""HELP"""


async def get_help(message: Message, apscheduler: AsyncIOScheduler) -> None:

    """
    The get_help function is responsible for handling the /help command.
    It will send a picture of the help_message to the user, and then schedule an asynchronous job
    to send them a message in two minutes. The show_jobs function is used to print out all
    the jobs that are currently scheduled.

    :param message: Message: Get the user id, so that we can send a message to him
    :param apscheduler: AsyncIOScheduler: Add a job to the scheduler
    :return: None; Send a picture with a description of the bot's capabilities
    """
    await get_picture(message.from_user.id, bot, help_message, 'help')
    user_id = (await check_user(message.from_user.id))[0]
    if user_id:
        apscheduler.add_job(send_message_chat_gpt, trigger='date',
                            run_date=datetime.now() + timedelta(minutes=2),
                            kwargs={'message': message})
        await show_jobs()
    else:
        await remind_about_auth(message.from_user.id)


async def show_jobs() -> None:
    """
    The show_jobs function is a coroutine that calls the sync_to_async function
    which wraps the synchronous show_job function. The asyncio event loop will run
    the wrapped synchronous show_job function in a thread pool executor. This allows
    the asynchronous code to call blocking functions without blocking the event loop.
    The show_jobs function is used to print out all the jobs that are currently scheduled.

    :return: None
    """
    async_show_jobs = sync_to_async(sync_show_job)
    try:
        await async_show_jobs()
    except BotException as error:
        print(error.__class__, error)


"""OFF"""


@sync_to_async
def profile_delete(id_user: int) -> None:
    """
    The profile_delete function deletes a profile from the database.


    :param id_user: int: Identify the user
    :return: None
    """
    try:
        Profile.objects.get(telegram_chat_id=id_user).delete()
        print('___ПРОФІЛЬ ВИДАЛЕНО___')
    except BotException as e:
        print(e.__class__, e)


async def disabling_authentication(message: Message) -> None:
    """
    The disabling_authentication function is used to delete the user's profile from the database.
        The function checks if a user has already registered in the bot, and if so, deletes his profile.
        If not, it sends a message that he is not registered.

    :param message: Message: Get the message that was sent to the bot
    :return: None
    """
    user_id, user_name = await check_user(message.from_user.id)
    if user_id:
        await profile_delete(message.from_user.id)
        message_to_user = f'{user_name}, Ваша реєстрація анульована. Для відновлення використовуйте команду /auth.'
        await get_picture(message.from_user.id, bot, message_to_user, 'off')
    else:
        message_to_user = f'{message.from_user.full_name},Ви ще не зареєстровані в боті. Дивиться команду /help.'
        await message.answer(message_to_user)
