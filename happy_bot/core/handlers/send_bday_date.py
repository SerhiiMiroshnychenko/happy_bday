from aiogram import Bot

from happy_bot.core.handlers.send_media import get_birthday_photo
from happy_bot.core.utils.named_tuple_classes import BDinfo


async def send_birthday_date(bot: Bot, chat_id: int, birthday: BDinfo):
    message = f'<b>{birthday.title.upper()}</b>\n' \
              f'{birthday.content}\n' \
              f'<b>{birthday.birth_date.strftime("%d.%m.%Y")}</b>\n' \
              f'Виповнюється:  <b>{birthday.age}</b> років\n\n' \

    if birthday.photo_path:
        await get_birthday_photo(chat_id, bot, message, birthday.photo_path)
    else:
        await bot.send_message(chat_id, message)
