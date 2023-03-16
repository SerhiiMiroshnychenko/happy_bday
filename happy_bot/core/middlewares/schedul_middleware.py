"""SCHEDULER MIDDLEWARE"""

# Базові імпорти
from typing import Dict, Any, Callable, Awaitable

# Імпорти Aiogram
from aiogram import BaseMiddleware
from aiogram.types.base import TelegramObject

# Планувальник
from apscheduler.schedulers.asyncio import AsyncIOScheduler


class SchedulerMiddleware(BaseMiddleware):
    """
    Generic middleware class for all types handlers
    """
    def __init__(self, scheduler: AsyncIOScheduler):
        """
        The __init__ function is called when the class is instantiated.
        It sets up the scheduler for use by other functions in this class.

        :param self: Represent the instance of the class
        :param scheduler: AsyncIOScheduler: Create a new instance of the class
        :return: Nothing
        """
        self.scheduler = scheduler

    async def __call__(
            self,
            handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
            event: TelegramObject,
            data: Dict[str, Any]) -> Any:
        """
        Execute middleware

        :param handler: Wrapped handler in middlewares chain
        :param event: Incoming event (Subclass of :class:`aiogram.types.base.TelegramObject`)
        :param data: Contextual data. Will be mapped to handler arguments
        :return: :class:`Any`
        """
        data['apscheduler'] = self.scheduler
        return await handler(event, data)
