from django import forms
from django.core.exceptions import ValidationError
from .models import BDays, Reminder


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
