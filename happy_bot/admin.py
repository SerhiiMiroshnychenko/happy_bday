"""РЕЄСТРАЦІЯ МОДЕЛІ PROFILE"""
from django.contrib import admin
from happy_bot.models import Profile


# Register the Profile model
@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'telegram_chat_id')  # Перелік полів,
    # які ми хочемо бачити в адмін-панелі
    list_display_links = ('user', 'telegram_chat_id')  # Поля за якими можна перейти на відповідну статтю
    search_fields = ('user',)  # За якими полями можна буде проводити пошук
    list_filter = ('user',)  # Призначаємо поля для фільтрації списку статей
