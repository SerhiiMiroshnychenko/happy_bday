"""РЕЄСТРАЦІЯ МОДЕЛІВ ДОДАТКУ HAPPY SITE"""
from django.contrib import admin
from happy_site.models import BDays, Reminder


# Register birthday and reminder models.
@admin.register(BDays)
class BDaysAdmin(admin.ModelAdmin):
    """
    Модель для імплементації записів про дні народження
    """
    list_display = ('id', 'title', 'content', 'photo', 'date', 'user')  # Перелік полів,
    # які ми хочемо бачити в адмін-панелі
    list_display_links = ('id', 'title')  # Поля за якими можна перейти на відповідну статтю
    search_fields = ('title',)  # За якими полями можна буде проводити пошук
    list_filter = ('user',)  # Призначаємо поля для фільтрації списку статей
    date_hierarchy = 'date'


@admin.register(Reminder)
class ReminderAdmin(admin.ModelAdmin):
    """
    Модель для імплементації нагадувань до днів народження
    """
    list_display = ('id', 'text', 'date_time', 'bday')
    list_filter = ('bday__user',)
    list_display_links = ('id', 'bday')
    search_fields = ('bday__title',)
    date_hierarchy = 'date_time'
