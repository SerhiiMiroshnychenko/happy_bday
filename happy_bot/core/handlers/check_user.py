from asgiref.sync import sync_to_async
from django.contrib.auth.models import User
from happy_site.models import BDays, Reminder

from happy_bot.models import Profile


@sync_to_async
def check_user(telegram_id) -> tuple:
    """
    Перевірка чи існує користувач в базі даних сайту
    та отримання його id та username.
    :param telegram_id:
    :return:
    """
    user_name = None
    user_id = None
    try:
        user = Profile.objects.filter(telegram_chat_id=telegram_id)
        user_name = user.first().user.username
        user_id = user.first().user.id
    except BaseException as e:
        print(e.__class__, e)
    return user_id, user_name


def is_user_in_bot(bday_id):

    user_id = BDays.objects.get(id=bday_id).user_id
    try:
        return Profile.objects.get(user_id=user_id).telegram_chat_id
    except BaseException as e:
        print(e.__class__, e)


def rem_id_to_bd_id(rem_id):
    return Reminder.objects.get(id=rem_id).bday_id





