import os
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ParseMode
from aiogram.utils import executor
from datetime import datetime, time, timedelta
from pytz import timezone
from django.conf import settings
from myapp.models import BDays

# ініціалізуємо токен бота і об'єкт бота
bot = Bot(token=os.environ['BOT_TOKEN'], parse_mode=ParseMode.HTML)
# ініціалізуємо об'єкт диспетчера
dp = Dispatcher(bot, storage=MemoryStorage())
# встановлюємо рівень логування
logging.basicConfig(level=logging.INFO)


# створюємо клас станів для FSM (Finite State Machine)
class BirthdaysStates(StatesGroup):
    waiting_for_birthday_date = State()


# функція, що повертає час у форматі "години:хвилини:секунди"
def get_current_time():
    tz = timezone(settings.TIME_ZONE)
    return datetime.now(tz).strftime('%H:%M:%S')


# функція, що відправляє нагадування про день народження користувача
async def send_birthday_reminder(bday, chat_id):
    message = f"Сьогодні {bday.title} виповнює {bday.get_age()} років! 🎉🎂🎈"
    if bday.content:
        message += f"\n<b>Опис:</b> {bday.content}"
    await bot.send_photo(chat_id=chat_id, photo=bday.photo, caption=message)


# функція, яка шукає у базі даних записи про дні народження, що відповідають сьогоднішній даті
async def find_birthdays():
    today = datetime.now().date()
    bdays = BDays.objects.filter(date__month=today.month, date__day=today.day)
    return bdays


# функція-хендлер, яка відповідає на команду /start
@dp.message_handler(Command('start'))
async def start(message: types.Message):
    chat_id = message.chat.id
    await message.answer(f"Привіт, {message.from_user.first_name}!"
                         f" Я бот, який буде надсилати нагадування про дні народження.")