from django.db.models.signals import post_delete
from django.dispatch import receiver
from happy_site.models import Reminder
from happy_bot.core.bot_scheduler.add_reminders import make_reminders_for_id
from happy_bot.bd_bot import bot
from happy_bday.settings import ADMIN_ID


@receiver(post_delete, sender=Reminder)
async def delete_reminder(sender, instance, **kwargs):
    """
    Функція, яка викликає make_reminders_for_id при видаленні нагадування.
    """
    print('\n\n___SIGNAL!___\n\n')
    print(f'{instance=}')
    chat_id = ADMIN_ID
    await make_reminders_for_id(bot, chat_id)
