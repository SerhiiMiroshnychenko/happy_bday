import json

from aiogram import Bot
from aiogram.types import Message
from asgiref.sync import sync_to_async

from happy_bday.settings import ADMIN_ID
from happy_bot.core.keyboards.inline import get_ukr_keyboard
from happy_bot.core.utils.commands import set_commands

from happy_bot.models import Profile

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from happy_bot.core.handlers.schedul_task import send_message_glory
from datetime import datetime, timedelta
from happy_bot.core.bot_scheduler.add_reminders import make_reminders_for_id

from happy_bot.core.handlers.check_user import check_user


async def start_bot(bot: Bot):
    await set_commands(bot)
    text = 'Бот запушено.'
    print(text)
    await bot.send_message(ADMIN_ID, text=text)
    users = await get_users()
    if users:
        for user in users:
            await make_reminders_for_id(bot=bot, chat_id=user.telegram_chat_id)


@sync_to_async
def get_users():

    users = None
    try:
        users = Profile.objects.all()
        for user in users:
            print(f'{user=}')
            print('Chat id:', user.telegram_chat_id)
    except BaseException as e:
        print(e.__class__, e)

    return users


async def stop_bot(bot: Bot):
    text = 'Бот зупинено.'
    print(text)
    await bot.send_message(ADMIN_ID, text=text)


async def write_file(content):
    with open('happy_bot/message_arg.json', 'w') as f:
        json.dump(content, f, indent=4, default=str)


async def get_photo(message: Message, bot: Bot):
    """
    Реакція на надсилання користувачем картинки
    та її збереження
    """
    await message.answer('Відмінно, Ти відправив фото. Я збережу його.')
    file_ = await bot.get_file(message.photo[-1].file_id)  # Зберігаємо об'єкт "file"
    # в атрибуті "photo" ми маємо три варіанти картинки різного розміру
    # отримаємо останній => найбільшого розміру
    print(f'PHOTO від {message.from_user.full_name}; Розмір: {message.photo[-1].file_size/1000} kb.')

    await bot.download_file(file_.file_path, 'download_media/photo')  # Завантажуємо файл з указанням його ім'я
    # та (за необхідності) шляху куди файл зберігати


async def get_glory(message: Message, bot: Bot, apscheduler: AsyncIOScheduler):
    """
    Реакція на повідомлення з текстом "Слава Україні"
    """
    print(f'MESSAGE від {message.from_user.full_name}:'
          f' "{message.text}".')
    await message.answer('Героям Слава!')
    apscheduler.add_job(send_message_glory, trigger='date',
                        run_date=datetime.now() + timedelta(seconds=8),
                        kwargs={'bot': bot, 'chat_id': message.from_user.id})


async def get_glory_answer(message: Message, bot: Bot):
    """
    Реакція на повідомлення з текстом "Смерть ворогам"
    """
    print(f'MESSAGE від {message.from_user.full_name}:'
          f' "{message.text}".')
    await message.answer('<b>ПЕРЕМОЗІ БУТИ</b>!', reply_markup=get_ukr_keyboard())


async def get_message(message: Message, bot: Bot):
    """
    Реакція на повідомлення
    """
    print(f'MESSAGE від {message.from_user.full_name}:'
          f' "{message.text}".')
    json_message = message.dict()
    await write_file(json_message)
    await message.reply(f'Тобі також: "<i>{message.text}</i>", <b>{message.from_user.full_name}</b>!')



