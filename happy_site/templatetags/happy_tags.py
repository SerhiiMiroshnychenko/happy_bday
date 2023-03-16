"""ТЕГ ДЛЯ ВІДОБРАЖЕННЯ НАГАДУВАНЬ"""

# Загальні імпорти
import pytz

# Імпорти Django
from django import template
from django.urls import reverse
from django.utils.html import format_html
from django.utils.safestring import SafeString

# Імпорти з пакета налаштувань
from happy_bday.settings import TIME_ZONE

# Внутрішні імпорти
from happy_site.models import BDays
from happy_site.views import get_reminders_by_birthday


register = template.Library()


@register.simple_tag
def reminders_for_birthday(birthday: BDays) -> SafeString | str:
    """
    The reminders_for_birthday function returns a string of HTML code
    that contains all the reminders for a given birthday.
    The function takes one argument, which is an instance of the BDays model class.
    The function uses this argument to get all Reminder objects associated
    with this particular birthday and then creates an HTML string containing
    links to edit these reminders and delete them.

    :param birthday: BDays: Get the reminders for a birthday
    :return: A string with html code
    """
    if not (reminders := get_reminders_by_birthday(birthday).order_by('date_time')):
        return ''
    html = "<p style='font-weight: bold; color: steelblue; text-align: left;'>Пам'ятки:</p>"
    for reminder in reminders:
        url = reverse('edit_reminder', args=[reminder.id])

        html += f'<div style="margin: 10px; padding: 10px"><a class="btn btn-secondary" ' \
                f' href="{url}">{reminder.text} ' \
                f'{reminder.date_time.astimezone(tz=pytz.timezone(TIME_ZONE)).strftime("(%d.%m.%y) %H:%M")}</a>' \
                f'<a class="btn btn-secondary" style="background-color: #D8E8FC; color: rosybrown"' \
                f' href="/edit_reminder/{reminder.id}/delete" ' \
                f'onclick="return confirm(\'Ви впевнені, що хочете видалити це нагадування?\')"' \
                f'onmouseover="this.style.backgroundColor=\'rosybrown\'; this.style.color=\'white\'"  ' \
                f'onmouseout="this.style.backgroundColor=\'#D8E8FC\'; this.style.color=\'rosybrown\'">X</a></div>'
    return format_html(html)
