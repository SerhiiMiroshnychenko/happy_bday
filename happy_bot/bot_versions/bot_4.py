from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ParseMode
from aiogram.utils.exceptions import Unauthorized

from happy_bot.models import Profile
from django.contrib.auth.models import User


# Створюємо стан, в якому очікуємо відповідь від користувача на запит про логін та пароль
class AuthState(StatesGroup):
    username = State()
    password = State()

# Обробник команди /start, яка ініціює процес авторизації
async def start_command(message: types.Message):
    await message.answer("Введіть ваш логін:")
    await AuthState.username.set()

# Обробник відповіді користувача на запит про логін
async def auth_username(message: types.Message, state: FSMContext):
    # Зберігаємо логін користувача в стані
    await state.update_data(username=message.text)
    await message.answer("Введіть ваш пароль:")
    await AuthState.password.set()

# Обробник відповіді користувача на запит про пароль
async def auth_password(message: types.Message, state: FSMContext):
    # Отримуємо дані про користувача зі стану
    data = await state.get_data()
    username = data.get('username')
    password = message.text

    # Перевіряємо, чи є такий користувач у базі даних
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        await message.answer("Користувача з таким логіном не знайдено")
        await state.finish()
        return

    if not user.check_password(password):
        await message.answer("Неправильний пароль")
        await state.finish()
        return

    # Зберігаємо telegram_chat_id користувача в базі даних сайту
    try:
        profile = Profile.objects.get(user=user)
        profile.telegram_chat_id = str(message.chat.id)
        profile.save()
        await message.answer("Ваш telegram_chat_id було збережено в базі даних")
    except Profile.DoesNotExist:
        await message.answer("Сталася помилка, спробуйте ще раз")
    except Exception as e:
        await message.answer(f"Сталася помилка: {e}")

    await state.finish()
