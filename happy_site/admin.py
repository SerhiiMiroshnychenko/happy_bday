from django.contrib import admin
from .models import BDays, Reminder


# Register your models here.
@admin.register(BDays)
class BDaysAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'content', 'photo', 'date', 'user')  # Перелік полів,
    # які ми хочемо бачити в адмін-панелі
    list_display_links = ('id', 'title')  # Поля за якими можна перейти на відповідну статтю
    search_fields = ('title',)  # За якими полями можна буде проводити пошук
    list_filter = ('user',)  # Призначаємо поля для фільтрації списку статей
    date_hierarchy = 'date'


@admin.register(Reminder)
class ReminderAdmin(admin.ModelAdmin):
    list_display = ('id', 'text', 'date', 'bday')
    list_filter = ('bday__user',)
    list_display_links = ('id', 'bday')
    search_fields = ('bday__title',)
    date_hierarchy = 'date'
