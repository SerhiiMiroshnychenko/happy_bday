from django.apps import AppConfig


class HappyBotConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'happy_bot'

    def ready(self):
        import happy_bot.signals

