from django.db.models.signals import post_delete
from django.dispatch import receiver
from happy_site.models import Reminder


# @receiver(post_delete, sender=Reminder)
# async def delete_reminder(sender, instance, **kwargs):
#     """
#     Цей код створює функцію delete_reminder, яка нічого не робить.
#     Ми використовуємо цей код, щоб Django не викидав помилки про те,
#     що немає слухача сигналу в додатку happy_bot.
#     """
#     pass

