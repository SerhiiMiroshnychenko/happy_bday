from asgiref.sync import async_to_sync
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from happy_bot.core.bot_scheduler.schedule_block import scheduler, reminders_scheduler
from happy_site.models import Reminder
from happy_bot.core.bot_scheduler.update_reminders import update_reminders_for_id
from happy_bot.bd_bot import bot
from happy_bday.settings import ADMIN_ID
import asyncio


# @receiver(post_delete, sender=Reminder)
# def delete_reminder(sender, instance, **kwargs):
#     """
#     Функція, яка викликає make_reminders_for_id при видаленні нагадування.
#     """
#     update_reminders_for_signal()


@receiver(post_save, sender=Reminder)
def save_reminder(sender, instance, **kwargs):
    """
    Функція, яка викликає make_reminders_for_id при видаленні нагадування.
    """
    print('IN SIGNAL:')
    update_reminders_for_signal()


def update_reminders_for_signal():
    print('___SIGNAL!___')
    chat_id = ADMIN_ID
    sync_make_reminders_for_id = async_to_sync(update_reminders_for_id, force_new_loop=True)

    try:
        sync_make_reminders_for_id(bot, chat_id)
    except BaseException as error:
        print(error.__class__, error, 'sync_make_reminders_for_id')

    try:
        sync_show_job()
    except BaseException as error:
        print(error.__class__, error, 'sync_show_jobs')


def sync_show_job():
    jobs = scheduler.get_jobs()
    rems = reminders_scheduler.get_jobs()
    print('@'*80, '\nSCHEDULER')
    print(f'Всього: {len(jobs)} завдань.')
    for job in jobs:
        print(job)
    print('@' * 80, '\nREM SCHEDULER')
    print(f'Всього: {len(rems)} нагадувань.')
    for rem in rems:
        print(rem)
    print('@'*80)
