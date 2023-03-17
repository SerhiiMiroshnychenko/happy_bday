"""
SIGNALS ДЛЯ ВИКЛИКУ ОНОВЛЕНЬ ЗАВДАНЬ БОТА
ПРИ ВНЕСЕННІ ЗМІН У МОДЕЛІ НАГАДУВАНЬ НА САЙТІ
"""

# Планувальник
from apscheduler.job import Job

# Перетворення sync та async
from asgiref.sync import async_to_sync

# Імпорти Django
from django.dispatch import receiver
from django.db.models.signals import post_delete, post_save

# Імпорт з пакета налаштувань
from happy_bday.settings import ADMIN_ID

# Внутрішні імпорти
from happy_site.models import Reminder
from happy_site.site_exceptions import SiteException

# Імпорти з додатка HappyBot
from happy_bot.bd_bot import bot
from happy_bot.core.bot_scheduler.update_reminders import update_reminders_for_id
from happy_bot.core.bot_scheduler.schedule_block import scheduler, reminders_scheduler


# Функція, яка викликає make_reminders_for_id при видаленні нагадування.
@receiver(post_delete, sender=Reminder)
def delete_reminder(sender, instance, **kwargs) -> None:
    """
    The delete_reminder function is called when a Reminder object is deleted.
    It calls the update_reminders_for_signal function to update all reminders for that signal.

    :param sender: Specify the model class that will send the signal
    :param instance: Get the instance of the model that was deleted
    :param kwargs: Pass a variable number of keyword arguments to the function
    :return: None
    """
    update_reminders_for_signal()


# Функція, яка викликає make_reminders_for_id при видаленні нагадування.
@receiver(post_save, sender=Reminder)
def save_reminder(sender, instance, **kwargs) -> None:
    """
    The save_reminder function is a signal receiver that updates the reminders for an instance of Reminder.
    It does this by calling update_reminders_for_id with the id of the instance.

    :param sender: Specify the model class that will send the signal
    :param instance: Get the object that was just created
    :param kwargs: Pass a variable number of keyword arguments to the function
    :return: None
    """
    print('IN SIGNAL:')
    update_reminders_for_signal()


def update_reminders_for_signal() -> None:
    """
    The update_reminders_for_signal function is called when the signal SIGUSR2 is received.
    It updates reminders for the admin user and shows all jobs.

    :return: None
    """
    print('___SIGNAL!___')
    chat_id = ADMIN_ID
    sync_make_reminders_for_id = async_to_sync(update_reminders_for_id, force_new_loop=True)

    try:
        sync_make_reminders_for_id(bot, chat_id)
    except SiteException as error:
        print(error.__class__, error, 'sync_make_reminders_for_id')

    try:
        sync_show_job()
    except SiteException as error:
        print(error.__class__, error, 'sync_show_jobs')


def sync_show_job() -> None:
    """
    The sync_show_job function is used to display the current jobs in the scheduler and reminders_scheduler.
    It takes no arguments, and it does return None.

    :return: The number of jobs in the scheduler and reminders_scheduler
    """
    jobs = scheduler.get_jobs()
    rems = reminders_scheduler.get_jobs()
    sync_show_job_logging('\nSCHEDULER', jobs, ' завдань.')
    sync_show_job_logging('\nREM SCHEDULER', rems, ' нагадувань.')


def sync_show_job_logging(shed_name: str, type_jobs: list[Job], name_jobs: str) -> None:
    """
    The sync_show_job_logging function is used to print out the number of jobs in each shed and
    the names of those jobs. It takes two arguments: a string representing the name of the shed,
    and a list containing all Job objects in that shed.

    :param shed_name: str: Identify the shed
    :param type_jobs: list[Job]: Specify the type of jobs to be displayed
    :param name_jobs: str: Display the name of jobs
    :return: The number of jobs in the shed and their names
    """
    print('@'*80, shed_name)
    print(f'Всього: {len(type_jobs)}{name_jobs}')
    for job in type_jobs:
        print(job)
    print('@' * 80)
