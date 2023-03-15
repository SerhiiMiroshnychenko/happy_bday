"""ОБРОБНИКИ АВТОРИЗАЦІЇ"""

# Базові імпорти
from asgiref.sync import sync_to_async

# Імпорти Django
from django.contrib.auth import authenticate
from django.contrib.auth.models import User

# Імпорти Aiogram
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

# Внутрішні імпорти
from happy_bot.bd_bot import bot
from happy_bot.models import Profile
from happy_bot.core.handlers.basic import check_user
from happy_bot.core.handlers.send_media import get_picture
from happy_bot.core.states.auth_state import AuthState


async def process_auth_command(message: Message, state: FSMContext) -> None:
    """
    Функція, що починає процес авторизації
    Перериває state, якщо користувач вже авторизований
    :param message: Message
    :param state: FSMContext
    :return: None
    """
    user_id, user_name = await check_user(message.from_user.id)
    if user_id:
        message_to_user = f'<b>{user_name}</b>, Ви вже зареєстровані в боті.'
        await get_picture(message.from_user.id, bot, message_to_user, 'auth')
        await state.clear()
        return None
    await message.answer("Введіть Ваш логін:")
    await state.set_state(AuthState.waiting_for_username)


async def process_username(message: Message, state: FSMContext) -> None:
    """
    Друга функція процесу авторизації
    Зберігає username в state та запускає очікування пароля
    :param message: Message
    :param state: FSMContext
    :return: None
    """
    await message.answer("Введіть Ваш пароль:")
    await state.update_data(username=message.text)
    await state.set_state(AuthState.waiting_for_password)


async def process_password(message: Message, state: FSMContext) -> None:
    """
    Завершальна функція процесу авторизації
    Видає результати всього процесу
    Очищує state
    :param message: Message
    :param state: FSMContext
    :return: None
    """
    data = await state.get_data()
    username = data["username"]
    password = message.text

    if user := await get_user(username, password):
        telegram_chat_id = str(message.from_user.id)
        await set_telegram_chat_id(user, telegram_chat_id)
        message_to_user = f'<b>{username}</b>, Ви успішно авторизувалися в боті!'
        await get_picture(message.from_user.id, bot, message_to_user, 'auth')

    else:
        message_to_user = "Користувача з таким логіном та паролем не знайдено. " \
                          "Зареєструйтеся на сайті для отримання подальших послуг."
        await get_picture(message.from_user.id, bot, message_to_user, 'off')
    await state.clear()  # clear state after authorization check


@sync_to_async
def get_user(username: str, password: str) -> User or None:
    """
    Функція, що перевіряє автентифікацію користувача
    :param username: str
    :param password: str
    :return: User or None
    """
    user = None
    try:
        user = authenticate(username=username, password=password)
    except User.DoesNotExist as error:
        print(error.__class__, error)
    return user


@sync_to_async
def set_telegram_chat_id(user: User, telegram_chat_id: str) -> None:
    """
    Функція, що задає поле telegram_chat_id в профіль автентифікованого користувача
    :param user: User
    :param telegram_chat_id: str
    :return: None
    """
    Profile.objects.update_or_create(user=user, telegram_chat_id=telegram_chat_id)
