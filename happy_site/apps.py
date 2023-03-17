"""РЕЄСТРАЦІЯ ДОДАТКУ HAPPY SITE"""
from django.apps import AppConfig


class HappySiteConfig(AppConfig):
    """
    Class representing a Django application HappySite and its configuration.
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'happy_site'
    verbose_name = 'Happy B-day!'

    def ready(self):
        """
        This method code runs when Django starts.

        :param self: Represent the instance of the class
        :return: None
        """
        import happy_site.signals
