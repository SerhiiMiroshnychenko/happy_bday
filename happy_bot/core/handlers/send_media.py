import string

from aiogram import Bot
from aiogram.types import Message, FSInputFile


async def get_birthday_photo(chat_id: int, bot: Bot, text: str, photo_path: str):
    print(f'{photo_path=}')
    bday_path = fr'D:\Final_project\happy_bday\media\{photo_path}'
    try:
        birthday_photo = FSInputFile(path=bday_path,
                                     filename='BDayPerson.png')
        await bot.send_photo(chat_id, photo=birthday_photo, caption=text)
    except BaseException as error:
        print(error.__class__, error)
        await bot.send_message(chat_id, text)


async def get_picture(chat_id: int, bot: Bot, text: str = None, name: str = None):
    reminder_picture = FSInputFile(path=fr'D:\Final_project\happy_bday\media\pictures\{name}.png',
                                   filename=f'ItIs{name.title()}.png')
    await bot.send_photo(chat_id, photo=reminder_picture, caption=text)
