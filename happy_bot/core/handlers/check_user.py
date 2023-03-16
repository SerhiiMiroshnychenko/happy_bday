"""ФУНКЦІЇ ПЕРЕВІРКИ ТА ОТРИМАННЯ ПРОФІЛЮ КОРИСТУВАЧА"""

# Перетворення sync та async
from asgiref.sync import sync_to_async

# Імпорти Django
from django.contrib.auth.models import User

# Внутрішні імпорти
from happy_bot.bd_bot import bot
from happy_bot.models import Profile


@sync_to_async
def check_user(telegram_id: int) -> tuple:
    """
    The check_user function checks if a user exists in the database and returns his id and username.


    :param telegram_id: int: Get the user id from the database
    :return: A tuple of two values: user_id, user_name
    """
    user_name = None
    user_id = None
    try:
        user = Profile.objects.filter(telegram_chat_id=telegram_id)
        user_name = user.first().user.username
        user_id = user.first().user.id
    except AttributeError as e:
        print(e.__class__, e)
    return user_id, user_name


# Отримуємо об'єкт User по його id
@sync_to_async
def get_user_for_user_id(user_id: int) -> User or None:
    """
    The get_user_for_user_id function takes in a user_id and returns the User object associated with that id.
    If no such User exists, it returns None.

    :param user_id: int: Specify the type of data that is expected to be passed into the function
    :return: A User object or None
    """
    user = None
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist as e:
        print(e.__class__, e)
    return user


async def remind_about_auth(user_id: int) -> None:
    """
    The remind_about_auth function sends a message to the user reminding them that they are not registered.


    :param user_id: int: Send a message to the user for id
    :return: None
    """
    message_to_user = 'Нагадую, що Ви ще не зареєстровані.' \
                      ' Для доступу до всіх функцій пройдіть реєстрацію на сайті та в боті.'
    print(f'$$$$$$$$$$$$$$$$$   {message_to_user=}')
    await bot.send_message(user_id, message_to_user)
