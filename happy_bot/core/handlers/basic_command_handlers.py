from datetime import datetime, timedelta

from aiogram import Bot
from aiogram.types import Message

from happy_bot.models import Profile


from asgiref.sync import sync_to_async
from happy_bot.core.handlers.basic import check_user
from happy_bot.core.messages.bese_command_messages import help_message

from happy_bot.core.keyboards.reply import get_reply_keyboard

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from happy_bot.core.handlers.schedul_task import send_message_chat_gpt


"""START"""


async def get_start(message: Message):
    """Обробка натискання користувача на кнопку старт"""

    user_id, user_name = await check_user(message.from_user.id)
    print(f'{user_name=}')
    print(f'{user_id=}')

    start_message_for_auth = f'\U0001F916Вітаю, <b>{user_name} ({message.from_user.full_name})</b>,' \
                             f' чим можу допомогти?'

    start_message_for_not_auth = f'\U0001F916Вітаю, <b>{message.from_user.full_name}</b>, ' \
                                 f'я бот сайту <b>HAPPY B-DAYS</b>.\n' \
                                 f'Для ознайомлення з моїми можливостями оберіть команду "<b>/help</b>".'

    message_for_user = start_message_for_auth if user_id else start_message_for_not_auth
    print(f'{message_for_user=}')

    await message.answer(message_for_user, reply_markup=get_reply_keyboard())


"""HELP"""


async def get_help(message: Message, apscheduler: AsyncIOScheduler):
    await message.answer(help_message)
    apscheduler.add_job(send_message_chat_gpt, trigger='date',
                        run_date=datetime.now() + timedelta(seconds=60),
                        kwargs={'message': message})


"""OFF"""


@sync_to_async
def profile_delete(id_user):
    print(f'{id_user=}')
    try:
        Profile.objects.get(telegram_chat_id=id_user).delete()
        print('\n\n ___ПРОФІЛЬ ВИДАЛЕНО___ \n\n')
    except BaseException as e:
        print(e.__class__, e)


async def disabling_authentication(message: Message):
    user_id, user_name = await check_user(message.from_user.id)
    if user_id:
        await profile_delete(message.from_user.id)
        await message.answer(f'{message.from_user.full_name}, Ваша реєстрація анульована.'
                             f' Для відновлення використовуйте команду /auth.')
    else:
        await message.answer(f'{message.from_user.full_name},Ви ще не зареєстровані в боті. Дивиться команду /halp.')

