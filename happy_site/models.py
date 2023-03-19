"""МОДЕЛІ ДЛЯ САЙТУ HAPPY SITE"""

from datetime import date
from django.db import models
from django.db.models import QuerySet
from django.utils import timezone
from django.contrib.auth.models import User


# Happy site models.
class BDays(models.Model):
    """
    Клас-модель для імплементації дописів про дні народження
    """
    title = models.CharField(max_length=30)
    content = models.TextField(max_length=255, null=True, blank=True, verbose_name='Опис')
    photo = models.ImageField(null=True, blank=True, upload_to='photos/',
                              verbose_name='Фото')  # upload_to -> показує в який каталог і які підкаталоги
    # ми будемо завантажувати наші фото
    date = models.DateField(verbose_name='Дата народження')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Користувач')

    @property
    def month(self) -> int:
        """
        The month function returns the month of the date.

        :param self: Refer to the object itself
        :return: int: The month of the date
        """
        return self.date.month

    @classmethod
    def get_birthdays_by_month(cls, month: int) -> QuerySet:
        """
        The get_birthdays_by_month function returns a list of all birthdays that occur in the given month.

        :param cls: Pass the class object to the function
        :param month: int: Filter the objects by month
        :return: A QuerySet of all the birthdays that occur in a given month
        """
        return cls.objects.filter(date__month=month)

    def get_age(self) -> int:
        """
        The get_age function returns the age of a person on their birthday in the current year.

        :param self: Refer to the instance of the class
        :return: The age of the person on their birthday in the current year
        """
        today = date.today()
        return today.year - self.date.year

    def __str__(self) -> str:
        """
        The __str__ function is used to return a string representation of the object.
        This is useful for debugging and also for displaying objects in the shell.

        :param self: Represent the instance of the object itself
        :return: The title of the birthday
        """
        return self.title

    class Meta:
        verbose_name = 'День народження'
        verbose_name_plural = 'Дні народження'
        ordering = ['date__month', 'date__day', 'title']
        # сортуємо за місяцем, днем та title в адмін-панелі
        # та на сайті (в списку екземплярів моделі BDays)


class Reminder(models.Model):
    """
    Клас-модель для імплементації нагадувань до днів народження
    """
    text = models.TextField(blank=True, null=True, verbose_name='Текст повідомлення')
    date_time = models.DateTimeField(verbose_name='Дата та час нагадування')
    bday = models.ForeignKey(BDays, on_delete=models.CASCADE, verbose_name='День народження')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Користувач')

    def save(self, *args, **kwargs):
        """
        The save function is called when the model instance is saved.
        The save function checks if the text field has a value, and if not, it sets it to 'Заплановане нагадування:'.
        Then it calls super(Reminder, self).save(*args, **kwargs) which saves the model instance.

        :param self: Represent the instance of the object
        :param args: Send a non-keyword variable length argument list to the function
        :param kwargs: Pass keyword, variable-length argument list
        :return: None
        """
        if not self.text:
            self.text = 'Заплановане нагадування:'
        super(Reminder, self).save(*args, **kwargs)

    def __str__(self) -> str:
        """
        The __str__ function is used to return a string representation of the object.
        This is what you see when you print an object, or convert it to a string using str().
        The __str__ function should return a human-readable representation of the object.

        :param self: Represent the instance of the object itself
        :return: A string representation of the object
        """
        local_date_time = timezone.localtime(self.date_time)
        return f'Reminder for {self.bday.title} on {local_date_time.strftime("%d.%m.%Y %H:%M %Z")}'

    class Meta:
        verbose_name = 'Нагадування'
        verbose_name_plural = 'Нагадування'
        ordering = ['id']
