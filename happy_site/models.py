from django.db import models
from datetime import datetime
from django.contrib.auth.models import User


# Create your models here.
class BDays(models.Model):
    title = models.CharField(max_length=30, verbose_name='День народження')
    content = models.TextField(max_length=255, null=True, blank=True, verbose_name='Опис')
    photo = models.ImageField(upload_to='photos/',
                              verbose_name='Фото')  # upload_to -> показує в який каталог і які підкаталоги
    # ми будемо завантажувати наші фото
    # year = models.IntegerField(null=True, blank=True, verbose_name='Рік')
    # month = models.IntegerField(verbose_name='Місяць')
    # day = models.IntegerField(verbose_name='День')
    date = models.DateField(verbose_name='Дата народження')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Користувач')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'День народження'
        verbose_name_plural = 'Дні народження'
        ordering = ['title']  # Задаємо сортування в адмін-панелі
        # та на сайті (в списку екземплярів моделі BDays)


class Reminder(models.Model):
    text = models.TextField(default='', verbose_name='Текст повідомлення')
    date = models.DateField(verbose_name='Дата нагадування')
    bday = models.ForeignKey(BDays, on_delete=models.CASCADE, verbose_name='День народження')

    def save(self, *args, **kwargs):
        if not self.text:
            self.text = f'Нагадую про день народження {self.bday.title}: {self.date.strftime("%d.%m")}'
        super(Reminder, self).save(*args, **kwargs)

    def __str__(self):
        return f'{self.bday.title} - {self.date.strftime("%d.%m.%Y")}'

    class Meta:
        verbose_name = 'Нагадування'
        verbose_name_plural = 'Нагадування'
        ordering = ['id']

