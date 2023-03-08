from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command
from django.contrib.auth import authenticate
from django.core.exceptions import SynchronousOnlyOperation

from ..states.auth_state import AuthState
from happy_bot.models import Profile, User
from asgiref.sync import sync_to_async

from happy_bot.core.handlers.basic import check_user


async def process_auth_command(message: Message, state: FSMContext):
    user_id, user_name = await check_user(message.from_user.id)
    if user_name:
        await message.answer(f'<b>{user_name}</b>, ви вже зареєстровані в боті.')
        await state.clear()
        return
    await message.answer("Введіть Ваш логін:")
    await state.set_state(AuthState.waiting_for_username)


async def process_username(message: Message, state: FSMContext):
    await message.answer("Введіть Ваш пароль:")
    await state.update_data(username=message.text)
    await state.set_state(AuthState.waiting_for_password)


@sync_to_async
def get_user(username, password):
    user = None
    try:
        user = authenticate(username=username, password=password)
    except User.DoesNotExist as error:
        print(error.__class__, error)
    if not user:
        users = User.objects.all()
        for user in users:
            print(user.id, user.username, user.password)
    return user


@sync_to_async
def set_telegram_chat_id(user, telegram_chat_id):
    Profile.objects.update_or_create(user=user, telegram_chat_id=telegram_chat_id)


async def process_password(message: Message, state: FSMContext):
    data = await state.get_data()
    username = data["username"]
    password = message.text

    user = await get_user(username, password)

    if user:
        telegram_chat_id = str(message.from_user.id)

        await set_telegram_chat_id(user, telegram_chat_id)
        await message.answer("Ви успішно авторизувалися в боті!")

    else:
        await message.answer("Користувача з таким логіном та паролем не знайдено. "
                             "Зареєструйтеся на сайті для отримання подальших послуг.")

    await state.clear()  # clear state after authorization check


