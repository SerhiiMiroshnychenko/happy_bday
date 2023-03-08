from asgiref.sync import sync_to_async
from happy_bot.models import Profile


@sync_to_async
def check_user(telegram_id) -> tuple:
    user_name = None
    user_id = None
    try:
        user = Profile.objects.filter(telegram_chat_id=telegram_id)
        user_name = user.first().user.username
        user_id = user.first().user.id
    except BaseException as e:
        print(e.__class__, e)
    return user_id, user_name
