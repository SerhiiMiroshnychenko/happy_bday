import pytz
from django import forms
from django.core.exceptions import ValidationError
from .models import BDays, Reminder
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from happy_bday.settings import TIME_ZONE
from datetime import datetime


class AddBDayForm(forms.ModelForm):

    class Meta:
        model = BDays  # Зв'язуємо ModelForm з моделлю BDays
        # fields - список полів, які треба відтворити
        fields = ['title', 'content', 'photo', 'date']
        #  widgets - індивідуальні стилі для полів
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-input'}),
            'content': forms.Textarea(attrs={'cols': 39, 'rows': 6}),
            'date': forms.DateInput(format='%d.%m.%Y')

        }
        labels = {
            'title': 'Іменинник',
            'content': 'Опис',
            'photo': 'Фото',
            'date': 'Дата народження',
        }
        help_texts = {
            'title': 'Введіть назву події ( наприклад ПІБ іменинника)',
            'content': "Опис події (Необов'язкове поле)",
            'photo': "Фото іменинника (Необов'язкове поле).",
            'date': 'Введіть дату народження у форматі "день.місяць.рік" (dd.mm.yyyy).',
        }

    def clean_title(self):
        # Метод для користувацького валідатора. Повинен починатися з "clean_"
        title = self.cleaned_data['title']  # Отримаємо заголовок який ввів користувач
        if len(title) > 30:
            raise ValidationError('Довжина більша 30 символів')

        return title


class UpdateBDayForm(forms.ModelForm):
    class Meta:
        model = BDays
        fields = ['title', 'content', 'photo', 'date']


class UpdateReminderForm(forms.ModelForm):
    class Meta:
        model = Reminder
        fields = ['text', 'date_time']


class RegisterUserForm(UserCreationForm):
    username = forms.CharField(label='Логін', widget=forms.TextInput(attrs={'class': 'form-input'}))
    email = forms.EmailField(label='Email', required=False, widget=forms.EmailInput(attrs={'class': 'form-input'}))
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-input'}))
    password2 = forms.CharField(label='Повтор пароля', widget=forms.PasswordInput(attrs={'class': 'form-input'}))

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class LoginUserForm(AuthenticationForm):
    username = forms.CharField(label='Логін', widget=forms.TextInput(attrs={'class': 'form-input'}))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-input'}))


class ReminderForm(forms.ModelForm):
    days_before = forms.IntegerField(min_value=0, label='За скільки днів попереджати')
    time_of_day = forms.TimeField(label='Час нагадування', input_formats=['%H:%M'])

    class Meta:
        model = Reminder
        fields = ('text', 'days_before', 'time_of_day')
        labels = {
            'text': 'Текст повідомлення'
        }

