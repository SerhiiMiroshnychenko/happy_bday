from django.apps import AppConfig


class HappySiteConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'happy_site'
    verbose_name = 'Happy B-day!'

    def ready(self):
        import happy_site.signals
