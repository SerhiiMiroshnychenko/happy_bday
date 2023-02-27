from django import forms
from django.core.exceptions import ValidationError
from .models import BDays, Reminder
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User


class AddBDayForm(forms.ModelForm):

    class Meta:
        model = BDays  # Зв'язуємо ModelForm з моделлю BDays
        # fields - список полів, які треба відтворити
        fields = ['title', 'content', 'photo', 'date']
        #  widgets - індивідуальні стилі для полів
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-input'}),
            'content': forms.Textarea(attrs={'cols': 60, 'rows': 10}),
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
