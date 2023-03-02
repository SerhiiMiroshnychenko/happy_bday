from datetime import date
from django.db import models
from datetime import datetime
from django.contrib.auth.models import User


# Create your models here.
class BDays(models.Model):
    title = models.CharField(max_length=30, verbose_name='День народження')
    content = models.TextField(max_length=255, null=True, blank=True, verbose_name='Опис')
    photo = models.ImageField(null=True, blank=True, upload_to='photos/',
                              verbose_name='Фото')  # upload_to -> показує в який каталог і які підкаталоги
    # ми будемо завантажувати наші фото
    # year = models.IntegerField(null=True, blank=True, verbose_name='Рік')
    # month = models.IntegerField(verbose_name='Місяць')
    # day = models.IntegerField(verbose_name='День')
    date = models.DateField(verbose_name='Дата народження')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Користувач')

    @property
    def month(self):
        return self.date.month

    @classmethod
    def get_birthdays_by_month(cls, month):
        return cls.objects.filter(date__month=month)

    def get_age(self):
        """Return the age of the person on their birthday in the current year."""
        today = date.today()
        birthday = self.date.replace(year=today.year)
        if birthday < today:
            return today.year - self.date.year
        else:
            return today.year - self.date.year - 1

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'День народження'
        verbose_name_plural = 'Дні народження'
        ordering = ['date__month', 'date__day', 'title']
        # сортуємо за місяцем, днем та title в адмін-панелі
        # та на сайті (в списку екземплярів моделі BDays)


class Reminder(models.Model):
    text = models.TextField(default='', verbose_name='Текст повідомлення')
    date_time = models.DateTimeField(default=datetime.now(), verbose_name='Дата та час нагадування')
    bday = models.ForeignKey(BDays, on_delete=models.CASCADE, verbose_name='День народження')

    def save(self, *args, **kwargs):
        if not self.text:
            self.text = f'Нагадую про день народження {self.bday.title}: {self.date_time.strftime("%d.%m")}'
        super(Reminder, self).save(*args, **kwargs)

    def __str__(self):
        return f'Reminder for {self.bday.title} on {self.date_time.strftime("%d.%m.%Y %H:%M")}'

    class Meta:
        verbose_name = 'Нагадування'
        verbose_name_plural = 'Нагадування'
        ordering = ['id']

