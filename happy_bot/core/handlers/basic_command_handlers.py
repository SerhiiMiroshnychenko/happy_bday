from aiogram.types import Message

from happy_bot.core.handlers.basic import check_user
from happy_bot.core.messages.bese_command_messages import help_message


"""START"""


async def get_start(message: Message):
    """Обробка натискання користувача на кнопку старт"""

    user_id, user_name = await check_user(message.from_user.id)
    print(f'{user_name=}')
    print(f'{user_id=}')

    start_message_for_auth = f'\U0001F916Вітаю, <b>{user_name} ({message.from_user.full_name})</b>,' \
                             f' чим можу допомогти?!.'

    start_message_for_not_auth = f'\U0001F916Вітаю, <b>{message.from_user.full_name}</b>, я бот сайту <b>HAPPY B-DAYS</b>.\n' \
                                 f'Для ознайомлення з моїми можливостями оберіть команду "<b>/help</b>".'

    message_for_user = start_message_for_auth if user_id else start_message_for_not_auth
    print(f'{message_for_user=}')

    await message.answer(message_for_user)


"""HELP"""


async def get_help(message: Message):
    await message.answer(help_message)

