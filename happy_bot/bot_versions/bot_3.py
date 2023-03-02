from aiogram import Bot, Dispatcher, types
from aiogram.types import ParseMode
from aiogram.utils import executor
from django.conf import settings
from happy_site.models import BDays

bot = Bot(token=settings.TELEGRAM_BOT_TOKEN)
dp = Dispatcher(bot)


# Опис команди /set_chat_id
@dp.message_handler(commands=['set_chat_id'])
async def set_chat_id_handler(message: types.Message):
    user_id = message.from_user.id
    chat_id = message.chat.id
    bday_users = BDays.objects.filter(user__id=user_id)
    if bday_users.exists():
        bday_user = bday_users.first()
        bday_user.telegram_chat_id = chat_id
        bday_user.save()
        await message.reply("Ваш telegram_chat_id успішно збережений!")
    else:
        await message.reply("Для користувача не знайдено жодного дня народження. Спочатку додайте день народження.")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
