"""БАЗОВІ ЗАГАЛЬНІ HANDLERS"""

# Базові імпорти
import json
from datetime import datetime, timedelta

# Перетворення sync та async
from asgiref.sync import sync_to_async

# Планувальник
from apscheduler.schedulers.asyncio import AsyncIOScheduler

# Імпорти Aiogram
from aiogram import Bot
from aiogram.types import Message

# Імпорти Django
from django.db.models.query import QuerySet

# Імпорт з пакета налаштувань
from happy_bday.settings import ADMIN_ID

# Внутрішні імпорти
from happy_bot.models import Profile
from happy_bot.bot_exceptions import BotException
from happy_bot.core.utils.commands import set_commands
from happy_bot.core.keyboards.inline import get_ukr_keyboard
from happy_bot.core.handlers.schedule_task import send_message_glory
from happy_bot.core.bot_scheduler.update_reminders import update_reminders_for_id


async def start_bot(bot: Bot) -> None:
    """
    Обробник початку роботи бота.
    Задає основні команди.
    Надсилає відповідну інформацію адміну.
    Оновлює нагадування для всіх користувачів.

    :param bot: Bot
    :return: None
    """

    await set_commands(bot)
    text = 'Бот запущено.'
    await bot.send_message(ADMIN_ID, text=text)
    if users := await get_users():
        for user in users:
            await update_reminders_for_id(bot=bot, chat_id=user.telegram_chat_id)


@sync_to_async
def get_users() -> QuerySet or None:
    """
    Функція повертає користувачів зареєстрованих в боті.

    :return: QuerySet or None
    """

    users = None
    try:
        users = Profile.objects.all()
        for user in users:
            print(f'{user=}')
            print('Chat id:', user.telegram_chat_id)
    except BotException as e:
        print(e.__class__, e)
    return users


async def stop_bot(bot: Bot) -> None:
    """
    Обробник закінчення роботи бота.
    Надсилає відповідну інформацію адміну.

    :param bot: Bot
    :return: None
    """

    text = 'Бот зупинено.'
    await bot.send_message(ADMIN_ID, text=text)


async def get_glory(message: Message, apscheduler: AsyncIOScheduler) -> None:
    """
    The get_glory function is a reaction to the message with text "Слава Україні".


    :param message: Message: Get the message object
    :param apscheduler: AsyncIOScheduler: Schedule a job
    :return: None; Send the answer to the message with text "Слава Україні"
    """

    await message.answer('Героям Слава!')
    apscheduler.add_job(send_message_glory, trigger='date',
                        run_date=datetime.now() + timedelta(seconds=8),
                        kwargs={'chat_id': message.from_user.id})


async def get_glory_answer(message: Message) -> None:
    """
    The get_glory_answer function.
    Реакція на повідомлення з текстом "Смерть ворогам".

    :param message: Message: Get the message object, which contains information about the sender.
    :return: None; Send the string "ПЕРЕМОЗІ БУТИ"
    """

    await message.answer('<b>ПЕРЕМОЗІ БУТИ</b>!', reply_markup=get_ukr_keyboard())


async def write_file(content: dict) -> None:
    """
    The write_file function takes in a dictionary and writes it to the message_arg.json file.


    :param content: dict: Pass in the dictionary that is created from the message
    :return: None
    """
    with open('happy_bot/message_arg.json', 'w') as f:
        json.dump(content, f, indent=4, default=str)


async def get_message(message: Message) -> None:
    """
    Реакція на надсилання користувачем різних типів повідомлень
    """
    message_types = []
    if message.text:
        message_types.append(f'текст: " <b>{message.text}</b> ".')
    if message.photo:
        message_types.append(f'картинку розміром {int(message.photo[-1].file_size / 1000)} kb')
    if message.video:
        message_types.append('відео')
    if message.audio:
        message_types.append('аудіо')
    if message.sticker:
        message_types.append('стікер')
    if message.document:
        message_types.append('документ')
    if message.contact:
        message_types.append('контакт')
    if message.location:
        message_types.append('локацію')
    if message.voice:
        message_types.append('голосове повідомлення')
    if message.animation:
        message_types.append('анімацію')
    if message.caption:
        message_types.append(f'з описом: " <b>{message.caption}</b> ".')
    if not message_types:
        message_types.append('повідомлення')

    message_to_user = 'Ви відправили мені:'
    await message.answer(message_to_user)
    for message_type in message_types:
        await message.answer(f' - {message_type}')

    json_message = message.dict()
    await write_file(json_message)
