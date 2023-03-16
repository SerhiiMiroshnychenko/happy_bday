"""РЕЄСТРАЦІЯ ДОДАТКУ HAPPY BOT"""
from django.apps import AppConfig


class HappyBotConfig(AppConfig):
    """
    Class representing a Django application HappyBot and its configuration.
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'happy_bot'

    def ready(self) -> None:
        """
        This method code runs when Django starts.

        :param self: Represent the instance of the class
        :return: None
        """
        import happy_bot.signals

