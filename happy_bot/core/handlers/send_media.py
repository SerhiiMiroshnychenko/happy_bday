import string

from aiogram import Bot
from aiogram.types import Message, FSInputFile


async def get_reminder_picture(chat_id: int, bot: Bot, text: string = None):
    reminder_picture = FSInputFile(path=r'D:\Final_project\happy_bday\media\pictures\clock.png',
                                   filename='ItIsTime.png')
    await bot.send_photo(chat_id, photo=reminder_picture, caption=text)


async def get_birthday_photo(chat_id: int, bot: Bot, text: string, photo_path: string):
    print(f'{photo_path=}')
    bday_path = fr'D:\Final_project\happy_bday\media\{photo_path}'
    try:
        birthday_photo = FSInputFile(path=bday_path,
                                     filename='BDayPerson.png')
        await bot.send_photo(chat_id, photo=birthday_photo, caption=text)
    except BaseException as error:
        print(error.__class__, error)
        await bot.send_message(chat_id, text)
