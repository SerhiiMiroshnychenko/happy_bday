"""КОМАНДА MANAGE.PY ДЛЯ ЗАПУСКУ БОТА"""


# Базові імпорти
import asyncio
import logging

# Імпорти Django
from django.core.management.base import BaseCommand

# Внутрішні імпорти
from happy_bot.bd_bot import bot
from happy_bot.core.bot_dicpatcher.set_dispatcher import dp
from happy_bot.core.bot_scheduler.schedule_block import scheduler, reminders_scheduler


async def start() -> None:
    """
    The start function is the entry point for the bot.
    It starts a polling loop, which listens to incoming
    messages and calls handlers when necessary.

    :return: None; Init the bot object
    """
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - [%(levelname)s] - %(name)s - '
                               '(%(filename)s).%(funcName)s(%(lineno)d) - %(message)s'
                        )

    scheduler.start()
    reminders_scheduler.start()

    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


class Command(BaseCommand):
    """
    The class for bot's running
    """
    help = 'RUN COMMAND: python manage.py runbot'

    def handle(self, *args, **options) -> None:
        """
        The handle function is the entry point for command execution.
        It should perform any work required to execute the command, and return an exit code.
        The default implementation calls self.execute(), which simply raises NotImplementedError.

        :param self: Represent the instance of the class
        :param args: Pass a variable number of arguments to a function
        :param options: Pass in options from the command line
        :return: None; Starting the bot.
        """
        asyncio.run(start())
